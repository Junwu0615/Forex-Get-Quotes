# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-01-24
        -目的: 欲使 <模擬交易> 可有使用之數據
        -功能: 鎖定 XAUUSD ...等商品，並儲存 M1 M5 M15 H1 H4 D1 數個 Interval
        -訊息通知: Telegram / line: 2025-03-31 停止服務
        -用 Docker 佈署並依給定排程運行
FIXME   -參數
            PYTHONUNBUFFERED=1
            SAVE_PATH=./data
            SCHEDULE_SETTINGS=MTWTFss=06:00:00,MTWTFss=18:00:00
            SQL_SERVICE_BROKER_HOST=<ip,port>
            SQL_SERVICE_LOGIN_PASSWORD=<password>
            SQL_SERVICE_LOGIN_USER=<user>
"""
import os
from datetime import datetime

from package.base import BaseLogic
from package.token import TokenSettings
from developer.package.norm_function import DATE_YMD_ONE
from developer.package.interface import Interface
from developer.definition.state import State

class Entry(Interface):
    def __init__(self, do_time=None):
        do_time = do_time or []
        self.base = BaseLogic(self)
        self.line = TokenSettings.line()
        self.fmp = TokenSettings.fmp()
        self.telegram = TokenSettings.telegram()
        super().__init__(do_time)

    def config_once(self):
        pass

    def update_once(self):
        # FIXME Todo Target
        ret = State.ERR_UNKNOWN
        base_path = os.environ.get('SAVE_PATH')
        self.create_folder(base_path)

        # target = ['xauusd']
        target = ['xauusd', 'eurusd', 'usdjpy', 'btcusd', 'ethusd']
        # interval_list = ['M1']
        interval_list = ['M1', 'M5', 'M15', 'H1', 'H4', 'D1']
        try:
            for symbol in target:
                self.create_folder(f'{base_path}/{symbol.upper()}')
                for interval in interval_list:
                    self.log_warning(f'Now: {symbol.upper()} [{interval}]')
                    self.base.save_data(base_path, symbol, interval)

            report = 'telegram'
            send_message = (f"[{report.upper()}] Time: {str(datetime.now())[:10]} Save Data to json and in Database | "
                            f"Target List: {[i.upper() for i in target]}")
            self.base.send_message(report=report, content_text=send_message)
            self.log_warning(send_message)
            ret = State.OK

        except:
            self.log_error(exc_info=True)
        finally:
            return ret
                 
if __name__ == "__main__":
    do_time = os.environ.get('SCHEDULE_SETTINGS')
    do_time = ['MTWTFss=06:00:00', 'MTWTFss=18:00:00'] if do_time is None else do_time.split(',')
    entry = Entry(do_time)