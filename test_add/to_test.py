from flask import Flask, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_studyroom_status(search_query, mode):
    # mode 0 : 학관, mode 1 : T동, mode 2 : R동
    url = ['http://203.249.67.222/', 'http://203.249.65.81/', 'http://223.194.83.66/']
    url_to_studyroom_num = {
        url[0]: 4,
        url[1]: 4,
        url[2]: 1, 
    }
    base_url = url[mode]

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    browser.get(base_url)
    browser.implicitly_wait(10)
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # Table 찾기
    tables = soup.find_all("table", {"cellpadding": "0", "cellspacing": "0", "border": "0", "width": "100%"})
    
    if tables:
        studyroom_status = []
        for table in tables:
            rows = table.find_all("tr")
            for row in rows[2:]:  # 첫 두 행은 제목 행일 가능성이 높으므로 스킵
                cols = row.find_all("td")
                if len(cols) == 5:  # 열의 개수가 5개인 경우
                    room_name = cols[0].text.strip()
                    total_seats = cols[1].text.strip()
                    used_seats = cols[2].text.strip()
                    remaining_seats = cols[3].text.strip()
                    utilization_rate = cols[4].text.strip()
                    studyroom_status.append({
                        "room_name": room_name,
                        "total_seats": total_seats,
                        "used_seats": used_seats,
                        "remaining_seats": remaining_seats,
                        "utilization_rate": utilization_rate
                    })
    
        
        for status in studyroom_status:
            print(status)
    else:
        print("No tables found.")

    # 특정 <td> 요소 찾기
    td_element = soup.find("td", {"id": "tbl_table", "colspan": "2"})
    browser.quit()

    if td_element:
        return str(tables) + "\n\n" + str(td_element)
    else:
        return "Element not found."

@app.route('/')
def index():
    html_content = get_studyroom_status(search_query=None, mode=0)
    return render_template_string("""
    <html>
        <head>
            <title>Studyroom Status</title>
        </head>
        <body>
            {{ html_content | safe }}
        </body>
    </html>
    """, html_content=html_content)

if __name__ == '__main__':
    app.run(debug=True)
