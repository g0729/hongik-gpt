import schedule
import time
import pandas as pd
from scrapper import Scrapper
import json
from collections import OrderedDict

# Scrapper 클래스 인스턴스 생성
scraper = Scrapper()

# 학식 정보 크롤링 및 엑셀 파일 업데이트
def update_food_list():
    scraper.get_food_list()
    food_df = pd.read_json('food_list.json')
    food_df.to_excel('food_list.xlsx', index=False)
    print("학식 정보 업데이트 완료") # 테스트용 메세지

# 공지사항 크롤링 및 엑셀 파일 업데이트
def update_notice():
    scraper.get_notice()

    # 공지사항 중 중복되는 것 없애기
    with open("notice_list.json", "r") as f:
        notices = json.load(f)
    # 중복되는 공지 링크 기준으로 제거
    seen_links = set()
    unique_notices = []
    for notice in notices:
        if notice['link'] not in seen_links:
            unique_notices.append(notice)
            seen_links.add(notice['link'])
    # 중복 제거된 공지사항들 json 파일에 기록
    with open("notice_list.json", "w") as f:
        json.dump(unique_notices, f, ensure_ascii=False, indent="\t")

    notice_df = pd.DataFrame(unique_notices)
    notice_df.to_excel('notice_list.xlsx', index=False)
    print("공지사항 업데이트 완료")


# 열람실 정보 크롤링 및 엑셀 파일 업데이트
def uqdate_studyroom_status():
    scraper.get_studyroom_status(search_query='', mode=1)  # mode에 따라 T동, R동 등 선택
    studyroom_df = pd.read_json('studyroom_status.json')
    studyroom_df.to_excel('studyroom_status.xlsx', index=False)
    print("열람실 정보 업데이트 완료")

'''
# 학식 정보는 하루에 한 번 업데이트
schedule.every().day.at("07:00").do(update_food_list)

# 공지사항과 열람실 정보는 매 1시간마다 업데이트
schedule.every(1).hours.do(update_notice)
schedule.every(1).hours.do(uqdate_studyroom_status)                            

# 스크립트 무한 루프 실행
while True:
    schedule.run_pending()
    time.sleep(1)
'''

# 테스트용: 1분으로 설정하고 테스트
schedule.every().minutes.do(update_food_list)
schedule.every(1).minutes.do(update_notice)
schedule.every(1).minutes.do(uqdate_studyroom_status)      

# 테스트용: 모든 작업을 즉시 실행
schedule.run_all()