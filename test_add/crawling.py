from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)
BaseException

result_file = "result.txt"
f = open(result_file, "w")
base_url = "https://www.hongik.ac.kr/kr/life/seoul-cafeteria-view.do?articleNo=5414&restNo=3"

browser.get(base_url)
soup = BeautifulSoup(browser.page_source, "html.parser")
day_lists = soup.find("div", "b-cafeteria-diet-list").find_all("div", recursive=False)

for day in day_lists:
    diet_list = day.find("div").find_all("div", recursive=False)
    date = day.find("p").text
    print(date)
    f.write(date + "\n\n")
    for diet in diet_list:
        time = diet.find("p").text
        print(time)
        f.write(time + "\n\n")
        menu_list = diet.find_all("li")
        for menu in menu_list:
            print(menu.text.rstrip())
            f.write(menu.text.rstrip() + "\n")
f.close()
