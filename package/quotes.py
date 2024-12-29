# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 00:03:07 2024

@author: PC
"""
from datetime import datetime

from package.base import BaseLogic
from package.token import TokenSettings
from developers.package.norm_function import DATE_YMD_ONE
from developers.package.interface import Interface
from developers.model.TForexQuotes import TForexQuotesField, TableFormat

class GetQuotes(Interface):
    def __init__(self):
        Interface.__init__(self)
        self.base = BaseLogic(self)
        self.line = TokenSettings.line()
        self.fmp = TokenSettings.fmp()
        self.telegram = TokenSettings.telegram()

    def main(self):
        # FIXME Todo Target
        target = ['xauusd', 'eurusd', 'usdjpy', 'btcusd', 'ethusd']
        self.create_folder('./datasets')
        for symbol in target:
            self.create_folder(f'./datasets/{symbol.upper()}')
            for interval in ['M1', 'M5', 'M15', 'H1', 'H4', 'D1']:
                self.log_warning(f'now todo: {symbol.upper()} [{interval}]')
                self.base.save_data(symbol, interval)

        send_message = (f"Time: {str(datetime.now())[:10]} Save Data | "
                        f"Target List: {[i.upper() for i in target]}")
        self.base.send_message(key='telegram', content_text=send_message)
        print(send_message)