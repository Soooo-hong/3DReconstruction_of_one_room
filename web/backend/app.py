from flask import Flask,request,jsonify, render_template
from flask_cors import CORS
import os 
import time
import json 
import subprocess 

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
            template_folder= os.path.join(basedir,'../frontend/template'),
            static_folder= os.path.join(basedir,'../frontend/static'))
CORS(app)

@app.route('/')
def run_application() : 
    return render_template('application.html')

@app.route('/threeDpage')
def threeDpage():
    return render_template('threeDpage.html')

@app.route('/process', methods=['POST'])
def process_data() :
    # html로부터 데이터 받아오기 
    data = request.json.get('data')
    data = data[0]      

    result = run_crawling_script(data)
    #크롤링된 이미지가 저장이 되면 아래 함수가 돌아가야됨 
    image_dir = 'web/backend/crowling_images/room_3'
    wait_for_images(image_dir)
    
    run_dust3r_infer()
    
    return render_template('application.html' , result=result)

def run_crawling_script(input_data) : 
    input_data = json.dumps(input_data)
    result = subprocess.check_output(['python', 'web/backend/zigbang_web_crawling.py',input_data], text=True)
    # 크롤링 페이지 가서 input_data가 딕셔너리로 되어있으니깐 1개씩 접근필요 
    return result

def run_dust3r_infer() : 
    result = subprocess.check_output(['python', 'dust3r/dust3r/demo.py'])

def wait_for_images(image_dir,timeout= 60) : 
        start_time = time.time()
        while True : 
            if any(file.endswith(('.png', '.jpg', '.jpeg', '.gif')) for file in os.listdir(image_dir)):
                break
            if time.time()-start_time>timeout : 
                raise TimeoutError("이미지 저장이 완료되지 않았습니다.")
        time.sleep(1)  # 1초 대기 후 다시 확인
        
if __name__ == '__main__' : 
    app.run(debug=True)