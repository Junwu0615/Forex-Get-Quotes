# -*- coding: utf-8 -*-
"""
@author: PC
FIXME
    Update Time: 2024-12-29
    -目的: 欲使 <模擬交易> 可有使用之數據
    -功能: 鎖定 XAUUSD ...等商品，並儲存 M1 M5 M15 H1 H4 D1 數個 Interval
    -訊息通知: Telegram / line: 2025-03-31 停止服務
    -待完成: 將該服務用 Docker 佈署並常駐運行
"""
import time
from schedule import every, run_pending
from package.quotes import GetQuotes

def todo_main():
    quotes = GetQuotes()
    quotes.main()
    
def check_schedule(do_time):
    every().monday.at(do_time).do(todo_main)    # 星期一
    every().tuesday.at(do_time).do(todo_main)   # 星期二
    every().wednesday.at(do_time).do(todo_main) # 星期三
    every().thursday.at(do_time).do(todo_main)  # 星期四
    every().friday.at(do_time).do(todo_main)    # 星期五
    every().saturday.at(do_time).do(todo_main)  # 星期六
    every().sunday.at(do_time).do(todo_main)    # 星期天
                 
if __name__ == "__main__":
    # todo_main()
    check_schedule(do_time='06:00:00') # 06:00:00
    while True:
        run_pending()
        time.sleep(1)