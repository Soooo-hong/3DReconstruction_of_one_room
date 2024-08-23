import argparse
import math
import builtins
import datetime
import os
import torch
import numpy as np
import functools
import trimesh
import copy
from scipy.spatial.transform import Rotation
import sys 
sys.path.append(os.path.join(os.path.abspath(__file__),'.'))

from dust3r.inference import inference
from dust3r.image_pairs import make_pairs
from dust3r.utils.image import load_images, rgb
from dust3r.utils.device import to_numpy
from dust3r.viz import add_scene_cam, CAM_COLORS, OPENGL, pts3d_to_trimesh, cat_meshes
from dust3r.cloud_opt import global_aligner, GlobalAlignerMode

import matplotlib.pyplot as pl


def get_args_parser():
    parser = argparse.ArgumentParser()
    parser_url = parser.add_mutually_exclusive_group()
    parser_url.add_argument("--local_network", action='store_true', default=False,
                            help="make app accessible on local network: address will be set to 0.0.0.0")
    parser_url.add_argument("--server_name", type=str, default=None, help="server url, default is 127.0.0.1")
    parser_url.add_argument("--image_size", type=int, default=512, choices=[512, 224], help="image size")
    parser_url.add_argument("--server_port", type=int, help=("will start gradio app on this port (if available). "
                                                             "If None, will search for an available port starting at 7860."),
                            default=None)
    parser_weights = parser.add_mutually_exclusive_group(required=True)
    parser_weights.add_argument("--weights", type=str, help="path to the model weights", default=None)
    parser_weights.add_argument("--model_name", type=str, help="name of the model weights",
                                choices=["DUSt3R_ViTLarge_BaseDecoder_512_dpt",
                                         "DUSt3R_ViTLarge_BaseDecoder_512_linear",
                                         "DUSt3R_ViTLarge_BaseDecoder_224_linear"])
    parser.add_argument("--device", type=str, default='cuda', help="pytorch device")
    parser.add_argument("--tmp_dir", type=str, default=None, help="value for tempfile.tempdir")
    parser.add_argument("--silent", action='store_true', default=False,
                        help="silence logs")
    return parser


def set_print_with_timestamp(time_format="%Y-%m-%d %H:%M:%S"):
    builtin_print = builtins.print

    def print_with_timestamp(*args, **kwargs):
        now = datetime.datetime.now()
        formatted_date_time = now.strftime(time_format)

        builtin_print(f'[{formatted_date_time}] ', end='')  # print with time stamp
        builtin_print(*args, **kwargs)

    builtins.print = print_with_timestamp


# 3D 장면을 GLB 파일로 변환 
def _convert_scene_output_to_glb(outdir, imgs, pts3d, mask, focals, cams2world, cam_size=0.05,
                                 cam_color=None, as_pointcloud=False,
                                 transparent_cams=False, silent=False):  # glb파일로 변환
    assert len(pts3d) == len(mask) <= len(imgs) <= len(cams2world) == len(focals)
    pts3d = to_numpy(pts3d)
    imgs = to_numpy(imgs)
    focals = to_numpy(focals)
    cams2world = to_numpy(cams2world)

    scene = trimesh.Scene()

    # full pointcloud
    if as_pointcloud:
        pts = np.concatenate([p[m] for p, m in zip(pts3d, mask)])
        col = np.concatenate([p[m] for p, m in zip(imgs, mask)])
        pct = trimesh.PointCloud(pts.reshape(-1, 3), colors=col.reshape(-1, 3))
        scene.add_geometry(pct)
    else:
        meshes = []
        for i in range(len(imgs)):
            meshes.append(pts3d_to_trimesh(imgs[i], pts3d[i], mask[i]))
        mesh = trimesh.Trimesh(**cat_meshes(meshes))
        scene.add_geometry(mesh)

    # add each camera
    for i, pose_c2w in enumerate(cams2world):
        if isinstance(cam_color, list):
            camera_edge_color = cam_color[i]
        else:
            camera_edge_color = cam_color or CAM_COLORS[i % len(CAM_COLORS)]
        add_scene_cam(scene, pose_c2w, camera_edge_color,
                      None if transparent_cams else imgs[i], focals[i],
                      imsize=imgs[i].shape[1::-1], screen_width=cam_size)

    rot = np.eye(4)
    rot[:3, :3] = Rotation.from_euler('y', np.deg2rad(180)).as_matrix()
    scene.apply_transform(np.linalg.inv(cams2world[0] @ OPENGL @ rot))
    outfile = os.path.join(outdir, f'scene_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.glb')
    if not silent:
        print('(exporting 3D scene to', outfile, ')')
    scene.export(file_obj=outfile)
    return outfile


# 이미지로 3D 모델 생성 
def get_3D_model_from_scene(outdir, silent, scene, min_conf_thr=3, as_pointcloud=False, mask_sky=False,
                            clean_depth=False, transparent_cams=False, cam_size=0.05):

    if scene is None:
        return None
    # post processes
    if clean_depth:
        scene = scene.clean_pointcloud()
    if mask_sky:
        scene = scene.mask_sky()

    # get optimized values from scene
    rgbimg = scene.imgs
    focals = scene.get_focals().cpu()
    cams2world = scene.get_im_poses().cpu()
    # 3D pointcloud from depthmap, poses and intrinsics
    pts3d = to_numpy(scene.get_pts3d())
    scene.min_conf_thr = float(scene.conf_trf(torch.tensor(min_conf_thr)))
    msk = to_numpy(scene.get_masks())
    return _convert_scene_output_to_glb(outdir, rgbimg, pts3d, msk, focals, cams2world, as_pointcloud=as_pointcloud,
                                        transparent_cams=transparent_cams, cam_size=cam_size, silent=silent)


# 주어진 이미지 파일들로부터 3D 장면을 재구성 최종 3D 모델을 생성
def get_reconstructed_scene(outdir, model, device, silent, image_size, filelist, schedule, niter, min_conf_thr,
                            as_pointcloud, mask_sky, clean_depth, transparent_cams, cam_size,
                            scenegraph_type, winsize, refid, output_filename):

    imgs = load_images(filelist, size=image_size, verbose=not silent)
    if len(imgs) == 1:
        imgs = [imgs[0], copy.deepcopy(imgs[0])]
        imgs[1]['idx'] = 1
    if scenegraph_type == "swin":
        scenegraph_type = scenegraph_type + "-" + str(winsize)
    elif scenegraph_type == "oneref":
        scenegraph_type = scenegraph_type + "-" + str(refid)

    pairs = make_pairs(imgs, scene_graph=scenegraph_type, prefilter=None, symmetrize=True)
    output = inference(pairs, model, device, batch_size=1, verbose=not silent)

    mode = GlobalAlignerMode.PointCloudOptimizer if len(imgs) > 2 else GlobalAlignerMode.PairViewer
    scene = global_aligner(output, device=device, mode=mode, verbose=not silent)
    lr = 0.01

    if mode == GlobalAlignerMode.PointCloudOptimizer:
        loss = scene.compute_global_alignment(init='mst', niter=niter, schedule=schedule, lr=lr)

    output_path = os.path.join(outdir, output_filename)
    output_file = _convert_scene_output_to_glb(outdir, scene.imgs, to_numpy(scene.get_pts3d()), 
                                               to_numpy(scene.get_masks()), to_numpy(scene.get_focals().cpu()), 
                                               to_numpy(scene.get_im_poses().cpu()), cam_size=cam_size, 
                                               as_pointcloud=as_pointcloud, transparent_cams=transparent_cams, 
                                               silent=silent)
    os.rename(output_file, output_path)

    return output_path


# 모델 merge 
def merge_glb(files, output_dir, version):  
    if not files:
        return None
    
    meshes = [trimesh.load(file) for file in files]
    
    # 새로운 씬 생성 
    scene = trimesh.Scene()
    
    # 각 씬에 매쉬 추가 
    for i, mesh in enumerate(meshes):
        translation_matrix = trimesh.transformations.translation_matrix([i, 0, 0]) 
        mesh.apply_transform(translation_matrix)
        scene.add_geometry(mesh)
    
    output_file = os.path.join(output_dir, f"merged_scene_v{version}.glb")
    scene.export(output_file)
    
    return output_file


import os

def get_image_files_from_folder(folder_path):
    # 폴더 내의 모든 PNG 파일을 리스트로 반환
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.png')]


def main_demo(tmpdirname, model, device, image_size, server_name=None, server_port=None, silent=False):
    # 저장할 경로 지정
    output_dir = "web/frontend/static/glb"
    os.makedirs(output_dir, exist_ok=True)  # 디렉토리가 없으면 생성

    # 폴더 경로 리스트
    folders = [
        "web/backend/crowling_images/room_1",
        "web/backend/crowling_images/room_2",
        "web/backend/crowling_images/room_3"
    ]

    # 각 폴더에 있는 이미지 파일 리스트를 가져옴
    inputfiles_list = [get_image_files_from_folder(folder) for folder in folders if os.path.isdir(folder)]
    
    output_files = []

    # 각 폴더의 이미지 파일을 사용해 모델 실행 및 저장
    for idx, inputfiles in enumerate(inputfiles_list):
        output_filename = f"model{idx+1}.glb"
        output_file = get_reconstructed_scene(output_dir, model, device, silent, image_size,
                                              inputfiles, 
                                              "linear", 300, 3.0, False, False, True, False, 
                                              0.05, "complete", 1, 0, output_filename)
        output_files.append(output_file)
        print(f"Model {idx+1} output file: {output_file}")

    version = 1  # 버전 카운터 초기화

    # 미리 정의된 조합에 따라 병합 파일 생성
    combinations = [
        (0, 1),   # model1 + model2
        (0, 2),   # model1 + model3
        (1, 2),   # model2 + model3
        (0, 1, 2) # model1 + model2 + model3
    ]

    for combination in combinations:
        selected_files = [output_files[idx] for idx in combination]

        if len(selected_files) > 1:  # 최소 2개의 파일이 있을 때만 병합
            merged_file = merge_glb(selected_files, output_dir, version)
            print(f"Merged 3D model version {version} saved to: {merged_file}")
            version += 1  # 버전 증가

    print("All models and merged files have been generated.")


