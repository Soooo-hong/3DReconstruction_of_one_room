from flask import Flask,request,jsonify, render_template,send_from_directory
from flask_cors import CORS
import os 
import time
import json 
import subprocess 
import sys 
import shutil


basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dust3r'))

app = Flask(__name__,
            template_folder= os.path.join(basedir,'../frontend/template'),
            static_folder= os.path.join(basedir,'../frontend/static'))
CORS(app)

@app.route('/')
def run_application() : 
    return render_template('application.html')

@app.route('/web/frontend/static/glb/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('../frontend/static/glb/', filename)

@app.route('/threeDpage')
def threeDpage():
    return render_template('threeDpage.html')

@app.route('/process', methods=['POST'])
def process_data() :
    # html로부터 데이터 받아오기 
    data = request.json.get('data')
    data = data[0]      
    rooms_path = 'web/backend/crowling_images'
    delete_photos_from_rooms(rooms_path)
    result= run_crawling_script(data)



    #크롤링된 이미지가 저장이 되면 아래 함수가 돌아가야됨 
    image_dir = 'web/backend/crowling_images/room_2'
    wait_for_images(image_dir, rooms_path)
    #replace_photos_from_rooms(image_dir)
    run_dust3r_infer()
    render_html = render_template('application.html' , result=result)
    return jsonify(success=True)

def run_crawling_script(input_data) : 
    input_data = json.dumps(input_data)
    result = subprocess.check_output(['python', 'web/backend/zigbang_web_crawling.py',input_data], text=True)
    # 크롤링 페이지 가서 input_data가 딕셔너리로 되어있으니깐 1개씩 접근필요 
    return jsonify(success=True,result = result)

def run_dust3r_infer() : 
    result = subprocess.check_output(['python', 'dust3r/demo.py','--model_name','DUSt3R_ViTLarge_BaseDecoder_512_dpt'])

def wait_for_images(image_dir, rooms_path,timeout= 60) : 
        start_time = time.time()
        while True : 
            if any(file.endswith(('.png', '.jpg', '.jpeg', '.gif')) for file in os.listdir(image_dir)):
                break
            if time.time()-start_time>timeout : 
                replace_photos_from_rooms(rooms_path)
                #raise TimeoutError("이미지 저장이 완료되지 않았습니다.")
        time.sleep(1)  # 1초 대기 후 다시 확인
        
def delete_photos_from_rooms(base_path):
    # 삭제할 폴더 목록
    rooms = ['room_1', 'room_2', 'room_3']
    
    for room in rooms:
        room_path = os.path.join(base_path, room)
        
        if os.path.exists(room_path):
            # 폴더 내의 모든 파일을 확인
            for filename in os.listdir(room_path):
                # 이미지 파일 확장자 목록
                if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    file_path = os.path.join(room_path, filename)
                    try:
                        os.remove(file_path)
                        print(f'{file_path} 삭제됨')
                    except Exception as e:
                        print(f'오류 발생: {e}')
        else:
            print(f'{room_path} 폴더가 존재하지 않음')
        
def replace_photos_from_rooms(base_path):
    # 대상 방 리스트와 대체 방 리스트
    rooms = ['room_1', 'room_2', 'room_3']
    rep_rooms = ['replace_room_1', 'replace_room_2', 'replace_room_3']
    
    # 각 방에 대해 반복
    for room, rep_room in zip(rooms, rep_rooms):
        room_path = os.path.join(base_path, room)  # 현재 방의 경로
        rep_room_path = os.path.join(base_path, rep_room)  # 대체 방의 경로
        
        # 현재 방에 있는 파일의 개수를 확인
        image_files = [f for f in os.listdir(room_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # 파일이 3개 이하일 경우, 대체 방의 이미지를 복사
        if len(image_files) <= 3:
            print(f"{room}에 있는 파일 수가 3개 이하입니다. {rep_room}의 이미지를 복사합니다.")
            
            # 현재 방의 파일 삭제
            for f in image_files:
                os.remove(os.path.join(room_path, f))
            
            # 대체 방의 파일 복사
            rep_image_files = [f for f in os.listdir(rep_room_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            for rep_file in rep_image_files:
                src_file = os.path.join(rep_room_path, rep_file)
                dst_file = os.path.join(room_path, rep_file)
                shutil.copy(src_file, dst_file)



if __name__ == '__main__' : 
    app.run(debug=True)