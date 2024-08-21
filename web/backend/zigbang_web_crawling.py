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
import sys
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

input_things = sys.argv[1]

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
time.sleep(2)

# 작은 구역 선택 
markers = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[1]/div')
driver.execute_script("arguments[0].click();", markers)
time.sleep(2)

#방 클릭 버튼 -1 
search_room = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div[5]/div/div/div/div[1]/div[1]/div/div[3]')
driver.execute_script("arguments[0].click();", search_room)
time.sleep(3)

# 방사진 클릭 
photo_tabs =  driver.find_elements(By.CSS_SELECTOR, ".css-1dbjc4n.r-1niwhzg")

time.sleep(0.5)

# 사진 가져오기 
# images = driver.find_elements(By.CLASS_NAME, 'css-9pa8cd')
download_folder = 'crowling_images'

image_urls = []
for index,img in enumerate(photo_tabs):
    src = img.get_attribute('style')
    url_start = src.find("url(") + 4
    url_end = src.find(")", url_start) - 1
    image_url = src[url_start:url_end].replace("&quot;", "").strip()
    response = requests.get(image_url)

    if response.status_code == 200:
        image_path = os.path.join(download_folder, f"image_{index + 1}.jpg")
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {image_path}")
    else:
        print(f"Failed to download: {image_url}")
# output_dir = 'crowling_images'
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)
# for index, img_url in enumerate(image_urls):
#     try:
#         img_data = requests.get(img_url).content
#         with open(os.path.join(output_dir, f'image_{index + 1}.jpg'), 'wb') as img_file:
#             img_file.write(img_data)
#         print(f'Image {index + 1} downloaded: {img_url}')
#     except Exception as e:
#         print(f'Failed to download image {index + 1}: {e}')

time.sleep(10)


driver.quit()
