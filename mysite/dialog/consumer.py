from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from utils.intent import predict
from utils.FindAnswer import FindAnswer
from utils.scrapper import ChromeDriver, get_phone_number, get_studyroom_status
from .apps import DialogConfig
import time
import numpy as np

THRESHOLD = 0.6


# HTML 테이블 생성 함수
def generate_html_table(data):
    html = "<table border='1' cellpadding='5' cellspacing='0'>\n"
    # 첫 번째 줄 (헤더)
    html += "  <tr>\n"
    for header in data[0].values():
        html += f"    <th>{header}</th>\n"
    html += "  </tr>\n"

    # 데이터 행
    for row in data[1:]:
        html += "  <tr>\n"
        for value in row.values():
            html += f"    <td>{value}</td>\n"
        html += "  </tr>\n"

    html += "</table>\n"
    return html


class DialogConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        mode = int(text_data_json["mode"])

        pred, pred_sentence, cos_sim = predict(message)
        print(message, pred_sentence, mode, cos_sim)

        if mode == 0 and cos_sim < THRESHOLD:
            await self.send(text_data=json.dumps({"message": "무슨 말인지 모르겠어요", "mode": 0, "button": []}))
            return

        if mode == 0:  # 답변 주고 끝
            return_message, button_lst, mode = FindAnswer(pred)
        elif mode == 1:
            return_message, button_lst, mode = FindAnswer(pred)
        elif mode == 2:  # 열람실 현황 크롤링 후 return
            return_message = ""
            status_list = []

            if "학관" in message or "H" in message or "G" in message:
                status_list = get_studyroom_status(mode=0)
            elif "T" in message:
                status_list = get_studyroom_status(mode=1)
            elif "R" in message:
                status_list = get_studyroom_status(mode=2)

            if status_list:
                return_message = generate_html_table(status_list)
            else:
                return_message = "열람실 정보를 찾을 수 없습니다."
            button_lst = []
            mode = 0
        elif mode == 3:  # 연락처 크롤링 후 return

            d2 = await get_phone_number(message, 1)  # person

            if d2:
                return_message = f"{len(d2)}개의 연락처 검색 결과입니다. <br> <br>"
                for d in d2:
                    return_message += f"성명 : {d['name']} <br> 소속 : {d['belong']} <br> 직책 : {d['spot']} <br> 연락처 : {d['phone_num']} <br> <br>"
            else:
                return_message = "연락처를 찾을 수 없습니다."
            button_lst = []
            mode = 0
        elif mode == 4:
            d1 = await get_phone_number(message, 0)  # Office
            if d1:
                return_message = f"{len(d1)}개의 연락처 검색 결과입니다. <br> <br>"
                for d in d1:
                    return_message += f"소속 : {d['name']} <br> 연락처 : {d['phone_num']} <br> <br>"
            else:
                return_message = "연락처를 찾을 수 없습니다."
            button_lst = []
            mode = 0

        print(return_message, mode, button_lst)
        await self.send(text_data=json.dumps({"message": return_message, "mode": int(mode), "button": button_lst}))
