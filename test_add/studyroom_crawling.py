from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# ChromeDriver 경로 설정 및 브라우저 열기
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL (학관, T동, R동)
# driver.get('http://203.249.67.222/RoomStatus.aspx')
academy_studyroom_url = 'http://203.249.67.222/'
T_studyroom_url = 'http://203.249.65.81/'
R_studyroom_url = 'http://223.194.83.66/'

url_to_studyroom_num = {
    academy_studyroom_url : 4,
    T_studyroom_url : 4 ,
    R_studyroom_url : 1, 
}

def get_studyroom_status(url) :
    driver.get(url)

    # 페이지 로딩 시간 대기
    time.sleep(2)  # 필요에 따라 조정

    # 열람실 자리 현황 데이터 크롤링
    rows = driver.find_elements(By.XPATH, '//table[@cellpadding="0" and @cellspacing="0" and @width="100%"]/tbody/tr')
    num_kind = url_to_studyroom_num[url] + 1 # 마지막줄 계
    
    for row in rows[2:3+num_kind]:  # 첫 두 행은 제목 행이므로 건너뜁니다 + 그 다음 첫번째 줄은 기준
        columns = row.find_elements(By.TAG_NAME, 'td')
        if columns:
            room_name = columns[0].text
            total_seats = columns[1].text
            used_seats = columns[2].text
            available_seats = columns[3].text
            utilization_rate = columns[4].text
            print(f'Room: {room_name}, Total: {total_seats}, Used: {used_seats}, Available: {available_seats}, Utilization: {utilization_rate}')
    
    for row in rows[3+num_kind : 3 + num_kind + num_kind * 4] :
        print(row.text)

    # 브라우저 닫기
    driver.quit()

#get_studyroom_status(academy_studyroom_url)
get_studyroom_status(T_studyroom_url)
#get_studyroom_status(R_studyroom_url)
