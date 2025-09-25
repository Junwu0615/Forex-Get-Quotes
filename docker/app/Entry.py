# -*- coding: utf-8 -*-
"""
@author: PC
        -目的: 欲使 <模擬交易> 可有使用之數據
        -功能: 鎖定 XAUUSD ...等商品，並儲存 M1 M5 M15 H1 H4 D1 數個 Interval
        -訊息通知: Telegram / line: 2025-03-31 停止服務
        -用 Docker 佈署並依給定排程運行
FIXME   -參數
            PYTHONUNBUFFERED=1
            SAVE_PATH=./data
            SCHEDULE_SETTINGS=MTWTFss=06:00:00,MTWTFss=18:00:00
            SQL_SERVER_BROKER_HOST=<ip,port>
            SQL_SERVER_LOGIN_PASSWORD=<password>
            SQL_SERVER_LOGIN_USER=<user>
"""
from lib.utils import UtilsLogic
from developer.utils.normal import *
from developer.utils.telegram import *
from developer.modules.logger import Logger
from developer.modules.interface import Interface
from developer.modules.models.WorkStatus import Status
from developer.modules.models.TForexQuotes import TForexQuotesField, TForexQuotesFormat

MODULE_NAME = __name__.upper()

class Entry(Interface):
    def __init__(self, do_time=None, logger=None):
        do_time = do_time or []
        if logger is None:
            raise Exception('Logger 未設定，請先於 __main__ 中定義')

        self.logger = logger
        self.fmp = os.environ.get('FMP_TOKEN')
        self.base = UtilsLogic(self, logger)
        super().__init__(do_time, logger)


    def config_once(self):
        pass


    def update_once(self):
        # FIXME Todo Target
        ret = Status.ERR_UNKNOWN
        base_path = os.environ.get('SAVE_PATH')
        os.makedirs(base_path, exist_ok=True)

        target = ['xauusd']
        # target = ['xauusd', 'eurusd', 'usdjpy', 'btcusd', 'ethusd']
        interval_list = ['D1']
        # interval_list = ['M1', 'M5', 'M15', 'H1', 'H4', 'D1']
        try:
            for symbol in target:
                os.makedirs(f'{base_path}/{symbol.upper()}', exist_ok=True)
                for interval in interval_list:
                    self.logger.warning(f'[{MODULE_NAME}] Now: {symbol.upper()} [{interval}]')
                    self.base.save_data(base_path, symbol, interval)

            message = (f'[{MODULE_NAME} : save data in json and ms sql]\n'
                       f'    - Time : {str(get_now(hours=8, tzinfo=TZ_UTC_8))[:19]}\n'
                       f'    - Target List : {[i.upper() for i in target]}')

            send_message(message,
                         logger=self.logger,
                         bot_token=os.environ.get('TELEGRAM_BOT_TOKEN'),
                         chat_id=os.environ.get('TELEGRAM_CHAT_ID'))

            self.logger.warning(f'[{MODULE_NAME}] {send_message}')
            ret = Status.OK

        except Exception as e:
            self.logger.error(f'[{MODULE_NAME}] 執行發生錯誤')

        finally:
            return ret


if __name__ == "__main__":
    logger = Logger(console_name=f'.{__name__}_console',
                    file_name=f'.{__name__}')

    logger.info(logger.title_log(f'[{__name__}] 主程式啟動'))

    do_time = os.environ.get('SCHEDULE_SETTINGS')
    do_time = ['MTWTFss=06:00:00', 'MTWTFss=18:00:00'] \
        if do_time is None else do_time.split(',')
    entry = Entry(do_time, logger)