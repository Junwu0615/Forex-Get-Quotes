# -*- coding: utf-8 -*-
"""
@author: PC
FIXME
    Update Time: 2024-12-30
    -目的: 欲使 <模擬交易> 可有使用之數據
    -功能: 鎖定 XAUUSD ...等商品，並儲存 M1 M5 M15 H1 H4 D1 數個 Interval
    -訊息通知: Telegram / line: 2025-03-31 停止服務
    -待完成: 將該服務用 Docker 佈署並常駐運行
"""
from datetime import datetime

from package.base import BaseLogic
from package.token import TokenSettings
from developers.package.norm_function import DATE_YMD_ONE
from developers.package.interface import Interface
from developers.definition.state import State

class Entry(Interface):
    def __init__(self, todo_time: list=[]):
        self.base = BaseLogic(self)
        self.line = TokenSettings.line()
        self.fmp = TokenSettings.fmp()
        self.telegram = TokenSettings.telegram()
        super().__init__(todo_time)

    def config_once(self):
        pass

    def update_once(self):
        # FIXME Todo Target
        ret = State.UNKNOWN
        try:
            target = ['xauusd', 'eurusd', 'usdjpy', 'btcusd', 'ethusd']
            self.create_folder('./datasets')
            for symbol in target:
                self.create_folder(f'./datasets/{symbol.upper()}')
                for interval in ['M1', 'M5', 'M15', 'H1', 'H4', 'D1']:
                    self.log_warning(f'now todo: {symbol.upper()} [{interval}]')
                    self.base.save_data(symbol, interval)

            report = 'telegram'
            send_message = (f"[{report}] Time: {str(datetime.now())[:10]} Save Data to json and in Database | "
                            f"Target List: {[i.upper() for i in target]}")
            self.base.send_message(report=report, content_text=send_message)
            self.log_warning(send_message)
            ret = State.OK

        except:
            self.log_error(ERROR_TEXT, exc_info=True)
        finally:
            return ret
                 
if __name__ == "__main__":
    todo_time = ['MTWTFss=06:00:00', 'MTWTFss=18:00:00']
    entry = Entry(todo_time)