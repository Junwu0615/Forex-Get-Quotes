# -*- coding: utf-8 -*-
"""
@author: PC
        -目的: 回補歷史數據
"""
from lib.utils import UtilsLogic
from developer.utils.normal import *
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

        # ['xauusd', 'eurusd', 'usdjpy', 'btcusd', 'ethusd']
        target_list = os.environ.get('TARGET_LIST')
        target_list = ['xauusd'] if target_list is None else target_list.split(',')

        # ['M1', 'M5', 'M15', 'H1', 'H4', 'D1']
        interval_list = os.environ.get('INTERVAL_LIST')
        interval_list = ['D1'] if interval_list is None else interval_list.split(',')

        try:
            for symbol in target_list:
                os.makedirs(f'{base_path}/{symbol.upper()}', exist_ok=True)
                for interval in interval_list:
                    self.logger.warning(f'[{MODULE_NAME}] Now: {symbol.upper()} [{interval}]')
                    self.base.save_data(base_path, symbol, interval)

            message = (f'[{MODULE_NAME} : save data in json and ms sql]\n'
                       f'    - Time : {str(get_now(hours=8, tzinfo=TZ_UTC_8))[:19]}\n'
                       f'    - Target List : {[i.upper() for i in target_list]}')

            self.logger.warning(f'[{MODULE_NAME}] {message}')
            ret = Status.OK

        except Exception as e:
            self.logger.error(f'[{MODULE_NAME}] 執行發生錯誤')

        finally:
            return ret


if __name__ == "__main__":
    logger = Logger(console_name=f'.cover_history_console',
                    file_name=f'.cover_history',
                    use_docker=os.environ.get('LOG_PATH'))

    logger.info(logger.title_log(f'[{__name__}] 主程式啟動'))
    entry = Entry(None, logger)