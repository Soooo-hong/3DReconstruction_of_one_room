from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import re 
import os 
import json
import shutil

room_info = {}

bojeung_detail = {#전세금도 동일하게 적용
        '전체' : 0,
        '20억' : -7,
        '10억' : -33,
        '5억' :-51,
        '1억' : -139,
        '5000만원' : -188,
        '1000만원' : -226,
        '500만원' : -234,
        '300만원' : -246,
    }

walse_detail = {
    '전체' : 0,
    '500만원' : -12,
    '300만원' : -39,
    '200만원' : -80,
    '100만원' :-103,
    '50만원' : -155,
    '30만원' : -209
}

def budget_detail(typename):
    if typename == '전세':
        #전세금 입력
        while True : 
            bojeung = input('전세금 금액을 다음 중 입력 : 전체 , 20억, 10억, 5억, 1억, 5000만원, 1000만원, 500만원, 300만원 :'  )
            if bojeung  in bojeung_detail.keys():
                #(월세) 보증금 슬라이더 이동 
                slider = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div/div/div[5]/div[2]/div[3]')
                action = ActionChains(driver)
                
                action.click_and_hold(slider).move_by_offset(bojeung_detail[bojeung], 0).release().perform()

                time.sleep(3)
                break
            else:
                print('잘못된 입력입니다. 다시 입력하세요')
        

        
        
    else:
        while True : 
            bojeung = input('보증금 금액을 다음 중 입력 : 전체 , 20억, 10억, 5억, 1억, 5000만원, 1000만원, 500만원, 300만원 :'  )
            if bojeung  in bojeung_detail.keys():
                break
            else:
                print('잘못된 입력입니다. 다시 입력하세요')
        print()

        #(월세) 보증금 슬라이더 이동 
        slider = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div/div/div[5]/div[2]/div[3]')
        action = ActionChains(driver)
        action.click_and_hold(slider).move_by_offset(bojeung_detail[bojeung], 0).release().perform()

        time.sleep(1)

        #월세 입력
        while True : 
            walse = input('월세 금액을 다음 중 입력 : 전체 , 500만원, 300만원, 200만원, 100만원, 50만원, 30만원 :' ) 
            if walse  in walse_detail.keys():
                break
            else:
                print('잘못된 입력입니다. 다시 입력하세요')
                
                
        #(월세) 월세 슬라이더 이동        
        slider = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div/div/div[6]/div[1]/div[2]/div[2]/div[3]')
        action = ActionChains(driver)
        action.click_and_hold(slider).move_by_offset(walse_detail[walse], 0).release().perform()

        time.sleep(1)

def target_check():#검색조건에 맞는 방이 없는 경우 확인
    target_class = "css-1563yu1 r-aw03qq r-1wbh5a2 r-1w6e6rj r-159m18f r-1i10wst r-b88u0q r-vrz42v r-q4m81j r-13wfysu r-q42fyq r-1ad0z5i"
    room_count = '/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[2]/div'
    
    check_path = '//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[2]/div'
    #element = driver.find_element(By.CLASS_NAME, target_class)
    try:
        # 클래스명으로 요소 찾기
        #element = driver.find_element(By.CLASS_NAME, target_class)
        chech_element = driver.find_element(By.XPATH, check_path)
        target_text = " 0개"
        if target_text in chech_element.text:
            print("조건에 맞는 방이 없습니다. 재설정하여주세요.")
            return False
    except:
        return True
    return True


#방 사진 다운 
def room_image_down(room_num):
# 방사진 클릭 => 이미지만 뜨도록 
    photo_tabs = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[1]/div/div/div/div[1]/div[2]/div/div[2]')
    photo_tabs.click()
    
    output_dir = 'crowling_images'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    room_output_dir = '../../crowling_images/room_'+str(room_num)
    if not os.path.exists(room_output_dir):
        os.makedirs(room_output_dir)
    else:
        shutil.rmtree(room_output_dir)
        os.makedirs(room_output_dir)
        
    # 사진 가져오기 
    i=1
    image_urls = []
    while True:
        xpath = '/html/body/div[6]/div/div[2]/div/div/div[3]/div[2]/div/div/div['+str(i)+']/div/div/div/img'
        try :
            image = driver.find_element(By.XPATH, xpath)
            time.sleep(1)
            src = image.get_attribute('src')
            image_urls.append(src)
            i+=1
        except:
            break
        

    
        #for file in os.scandir(room_output_dir):
         #   os.remove(file.path)
            
            
    for index, img_url in enumerate(image_urls):
        try:
            img_data = requests.get(img_url).content
            with open(os.path.join(room_output_dir, f'room_{room_num}_image_{index + 1}.jpg'), 'wb') as img_file:
                img_file.write(img_data)
            print(f'Image {index + 1} downloaded: {img_url}')
            time.sleep(1)
        except Exception as e:
            print(f'Failed to download image {index + 1}: {e}')



# 크롬드라이버 실행
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # 최대화된 상태로 시작
#driver = webdriver.Chrome(executable_path= 'C:/chromedriver-win64/chromedriver-win64/chromedriver')
driver = webdriver.Chrome(options=chrome_options) 

#크롬 드라이버에 url 주소 넣고 실행W
driver.get('https://www.zigbang.com/home/oneroom/map')

# 페이지가 완전히 로딩되도록 3초동안 기다림
time.sleep(3)

# 검색어 창을 찾아 search 변수에 저장 (By.XPATH 방식)
wait = WebDriverWait(driver,10)
search_box = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[1]/div[1]/div/div[1]/input')

input_things = input('지역 입력하세요 : ')
search_box.send_keys(input_things)
time.sleep(2)

# 엔터 버튼 
search_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[1]/div[1]/div/div[2]/button')
driver.execute_script("arguments[0].click();", search_button)
time.sleep(2)

# 전월세 버튼 
search_button2 = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[3]/div/div[1]/div/div/div[1]/div[2]')
driver.execute_script("arguments[0].click();", search_button2)
time.sleep(1)


#전월세 여부 -> 나중엔 버튼으로
typename = input('전세, 월세 여부를 입력하세요 : ( ex, 전세 ) ')
if typename == '전세':
    while True:
        monthly_butoon = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div/div/div[2]/div/div[2]/div/div[2]')
        driver.execute_script("arguments[0].click();", monthly_butoon)
        time.sleep(3)
        
        # 작은 구역 선택 
        markers = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[1]/div')
        driver.execute_script("arguments[0].click();", markers)
        time.sleep(3)
        
            
        budget_detail(typename)#전세금 입력
        is_exist = target_check()
        if is_exist:
            break
        else:
            #초기화 버튼 클릭
            reset_button = driver.find_element(By.XPATH, '//*[@id="animatedComponent"]/div[2]')
            driver.execute_script("arguments[0].click();", reset_button)
    
    
        
    
else :
    while True:
        monthly_butoon = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div/div/div[2]/div/div[3]/div/div[2]')
        driver.execute_script("arguments[0].click();", monthly_butoon)
        time.sleep(3)
        
        # 작은 구역 선택 
        markers = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[1]/div')
        driver.execute_script("arguments[0].click();", markers)
        time.sleep(3)
        
        budget_detail(typename)#월세, 보증금 입력
        is_exist = target_check()
        if is_exist:
            break
        else:
            #초기화 버튼 클릭
            reset_button = driver.find_element(By.XPATH, '//*[@id="animatedComponent"]/div[2]')
            driver.execute_script("arguments[0].click();", reset_button)
   
    
    



#### 보류 ###########
#스크롤 내리기 
# actions = ActionChains(driver)
# element = driver.find_element(By.XPATH,  '//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]' )  # XPath로 요소 찾기
# drag = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div/div')
# drop = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div/div/div[6]')
# actions.drag_and_drop(drag, drop).perform()
# time.sleep(1)

# right_slider = driver.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-1mlwlqe.r-16y2uox.r-1q142lx.r-h0d30l.r-1777fci.r-ltgprq.r-1oa8saw.r-1v1z2uz')  # 슬라이더의 CSS 선택자
# # <div class="css-1dbjc4n r-n2h5ot r-1jkafct r-18u37iz r-hdaws3 r-dt9w19 r-bztko3 r-lrvibr"><div class="css-1dbjc4n" style="background-color: rgb(77, 77, 77); border-radius: 4px; flex-grow: 0; left: 0px; width: 284px; -webkit-box-flex: 0;"></div></div><div class="css-1dbjc4n r-14lw9ot r-5ekf5r" style="border-radius: 14px; border-width: 1px; box-shadow: rgba(26, 26, 26, 0.1) 0px 2px 2px; height: 28px; left: 0px; margin-left: -14px; position: absolute; user-select: none; width: 28px;"></div><div class="css-1dbjc4n r-14lw9ot r-5ekf5r" style="border-radius: 14px; border-width: 1px; box-shadow: rgba(26, 26, 26, 0.1) 0px 2px 2px; height: 28px; left: 284px; margin-left: -14px; position: absolute; user-select: none; width: 28px;"></div></div>
# def move_slider_to(slider, target_position):
#     actions = ActionChains(driver)
    
#     # 현재 위치 가져오기
#     current_position = slider.location['x']
#     distance_to_move = target_position - current_position
    
#     # 슬라이더를 원하는 위치로 이동
#     if distance_to_move > 0:
#         actions.click_and_hold(slider).move_by_offset(distance_to_move, 0).release().perform()
#     else:
#         actions.click_and_hold(slider).move_by_offset(distance_to_move, 0).release().perform()
    
#     time.sleep(0.1)  # 조정 속도 조절

# # 원하는 위치 설정 (예: 500px)
# desired_position = 100  # 원하는 위치에 맞게 조정하세요

# # 슬라이더를 해당 위치로 이동
# move_slider_to(right_slider, desired_position)
# time.sleep(5)
#####################################3

#방 클릭 버튼 => 오른쪽 가장 상단 방



room_num=1

room_search_path = ['//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div[5]/div/div/div','//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div[6]/div/div/div', '//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div[7]/div/div/div','//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div[10]/div/div/div','//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div[11]/div/div/div','//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div[12]/div/div/div','//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[4]/div/div/div','//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[5]/div/div/div','//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[6]/div/div/div' ,'//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[8]/div/div/div', '//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[9]/div/div/div', '//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[10]/div/div/div']
room_search_path_indx=0
while room_num<4:
    
    if room_search_path_indx>= len(room_search_path):
        break
    
    try :#방 클릭
        search_room = driver.find_element(By.XPATH, room_search_path[room_search_path_indx])
        search_room.click()
        time.sleep(3)
        
        room_image_down(room_num)
        room_num+=1
        
        try:
            #X버튼
            x_button = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div[2]/div/div/div[3]/div/div')
            x_button.click()
            time.sleep(2)
        except:
            print('x버튼 클릭 에러 ')
        
        try:
            #이전 버튼
            before_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div/div[3]/div[1]/div[1]/div/div[1]/div/div')
            
            before_button.click()
            time.sleep(2)
        except:
            print('이전 버튼 클릭 에러 ')
        
    except:
        
        
        print('room_click_error')
        
    room_search_path_indx+=1
    
    




"""
#elements = driver.find_elements(By.CSS_SELECTOR, '.css-1563yu1 r-aw03qq r-1wbh5a2 r-1w6e6rj r-159m18f r-1x35g6 r-b88u0q r-ueyrd6 r-fdjqy7 r-13wfysu r-q42fyq r-1ad0z5i')
try : 
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.css-1563yu1 r-aw03qq r-1wbh5a2 r-1w6e6rj r-159m18f r-1x35g6 r-b88u0q r-ueyrd6 r-fdjqy7 r-13wfysu r-q42fyq r-1ad0z5i'))
    )
    print(len(elements))
    for element in elements:
        print(element.text)
    input("정보 출력 끝2")
except :
    try : 
        elements = driver.find_elements(By.CLASS_NAME, 'css-1563yu1 r-aw03qq r-1wbh5a2 r-1w6e6rj r-159m18f r-1x35g6 r-b88u0q r-ueyrd6 r-fdjqy7 r-13wfysu r-q42fyq r-1ad0z5i')
        for element in elements:
            print(element.text)
        input("정보 출력 끝1")
    except:  
        print("응 없어~ㄴ")
          


paths = ['//*[@id="__next"]/div[2]/div/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[5]/div[2]/div[1]/div[2]/div', '//*[@id="__next"]/div[2]/div/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[5]/div[2]/div[2]/div[2]/div', '//*[@id="__next"]/div[2]/div/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[5]/div[2]/div[3]/div[2]/div', '//*[@id="__next"]/div[2]/div/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[5]/div[2]/div[4]/div[2]/div', '//*[@id="__next"]/div[2]/div/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[5]/div[2]/div[5]/div[2]/div', '//*[@id="__next"]/div[2]/div/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[5]/div[2]/div[6]/div[2]/div']

for i in range(len(paths)):
    
    try:
        #가격 정보 추출
        element = driver.find_element(By.XPATH, paths[i] )

        value = element.text
        room_info[str(i)+"번 째 정보"] =  element.text
        time.sleep(1)
    except:
        print(i, '에서 오류')


with open('roominfo.json', 'w', encoding='utf-8') as json_file:
    json.dump(room_info, json_file, ensure_ascii=False, indent=4)
"""
    
    
time.sleep(5)



driver.quit()
