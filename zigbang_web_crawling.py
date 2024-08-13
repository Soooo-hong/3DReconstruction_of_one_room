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

# 크롬드라이버 실행
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # 최대화된 상태로 시작

driver = webdriver.Chrome(options=chrome_options) 

#크롬 드라이버에 url 주소 넣고 실행
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

# 월세 버튼 클릭
monthly_butoon = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div/div/div[2]/div/div[3]/div/div[2]')
driver.execute_script("arguments[0].click();", monthly_butoon)
time.sleep(3)

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

#방 클릭 버튼 -1 
search_room = driver.find_element(By.CSS_SELECTOR, '[data-testid="원룸매물리스트_0"]')
driver.execute_script("arguments[0].click();", search_room)
time.sleep(3)

# 방사진 클릭 
photo_tabs = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/div/div/div/div[1]/div[2]/div/div[2]')
driver.execute_script("arguments[0].click();", photo_tabs)
time.sleep(0.5)

# 사진 가져오기 
images = driver.find_elements(By.CLASS_NAME, 'css-9pa8cd')
image_urls = []
for img in images:
    src = img.get_attribute('src')
    image_urls.append(src)

output_dir = 'crowling_images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
for index, img_url in enumerate(image_urls):
    try:
        img_data = requests.get(img_url).content
        with open(os.path.join(output_dir, f'image_{index + 1}.jpg'), 'wb') as img_file:
            img_file.write(img_data)
        print(f'Image {index + 1} downloaded: {img_url}')
    except Exception as e:
        print(f'Failed to download image {index + 1}: {e}')

time.sleep(10)


driver.quit()
