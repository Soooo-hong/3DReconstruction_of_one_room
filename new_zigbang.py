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

"""
#전월세 여부 -> 나중엔 버튼으로
momorchar = input('전체, 전세, 월세 여부를 입력하세요 : ( ex, 전세 ) ')
if momorchar == '전체':
    monthly_butoon = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div/div/div[2]/div/div[1]/div/div[2]')
    driver.execute_script("arguments[0].click();", monthly_butoon)
    time.sleep(3)
elif momorchar == '전세':
    monthly_butoon = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div/div/div[2]/div/div[2]/div/div[2]')
    driver.execute_script("arguments[0].click();", monthly_butoon)
    time.sleep(3)
else :
    monthly_butoon = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div/div/div[2]/div/div[3]/div/div[2]')
    driver.execute_script("arguments[0].click();", monthly_butoon)
    time.sleep(3)"""
    
# 월세 버튼 클릭
monthly_butoon = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div/div/div[2]/div/div[3]/div/div[2]')
driver.execute_script("arguments[0].click();", monthly_butoon)
time.sleep(3)

# 작은 구역 선택 
markers = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[1]/div')
driver.execute_script("arguments[0].click();", markers)
time.sleep(2)


#방 클릭 버튼 => 오른쪽 가장 상단 방
#search_room = driver.find_elements(By.CSS_SELECTOR, '[data-testid="원룸매물리스트_0"]')
search_room = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div[5]/div/div/div/div[1]/div[1]/div/div[3]')

driver.execute_script("arguments[0].click();", search_room)


#search_rooms = driver.find_elements(By.CSS_SELECTOR, '[data-testid="원룸매물리스트_0"]')

time.sleep(3)


# 방사진 클릭 => 이미지만 뜨도록 
photo_tabs = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[1]/div/div/div/div[1]/div[2]/div/div[2]')
photo_tabs.click()
                
    
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
    

output_dir = 'crowling_images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
for index, img_url in enumerate(image_urls):
    try:
        img_data = requests.get(img_url).content
        with open(os.path.join(output_dir, f'image_{index + 1}.jpg'), 'wb') as img_file:
            img_file.write(img_data)
        print(f'Image {index + 1} downloaded: {img_url}')
        time.sleep(1)
    except Exception as e:
        print(f'Failed to download image {index + 1}: {e}')

time.sleep(5)


driver.quit()
