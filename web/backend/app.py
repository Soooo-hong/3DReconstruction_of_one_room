from flask import Flask,request,jsonify, render_template
from flask_cors import CORS
import os 
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
    os.makedirs('web/inputdata',exist_ok=True)
    with open('web/inputdata.data.txt','a',encoding='utf-8') as f : 
        # for value in data[0].values() :
        #     f.write(value + '\n')
        # f.write("--------------------")
        data = list(data[0].values())      
          
    result = run_crawling_script(data[0])
    
    return render_template('application.html' , result=result)

def run_crawling_script(input_data) : 
    result = subprocess.check_output(['python', 'web/backend/zigbang_web_crawling.py',input_data], text=True)
    return result

if __name__ == '__main__' : 
    app.run(debug=True)