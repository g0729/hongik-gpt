from apscheduler.schedulers.background import BackgroundScheduler
import schedule
import time
from utils import updatefile
from utils import renew
from utils.FindAnswer import renew_df
import os
from configure import ANSWER_FILE_PATH, ANSWER_TEMPLATE_FILE_PATH, RENEW_FILE_PATH


## 2시간 마다 업데이트
def interval_job():
    print("Running interval job tasks...")
    updatefile.update_date(RENEW_FILE_PATH)
    updatefile.update_notice(RENEW_FILE_PATH)
    updatefile.update_weather(RENEW_FILE_PATH)
    run_renew()
    renew_df()


# 매일 정각에 업데이트
def daily_job():
    print("Running daily job tasks...")
    updatefile.update_food_list(RENEW_FILE_PATH)
    run_renew()
    renew_df()


def run_renew():
    print("Running renew tasks...")
    renew.replace_marker_and_save_new_file(ANSWER_TEMPLATE_FILE_PATH, RENEW_FILE_PATH, ANSWER_FILE_PATH)


def main():
    interval_job(),
    daily_job()
    sched = BackgroundScheduler()
    sched.add_job(interval_job, "interval", hours=2, id="every_2hour")
    sched.add_job(daily_job, "cron", hour="0", minute="5", id="daily")
    sched.start()
