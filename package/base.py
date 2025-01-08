# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 00:03:07 2024

@author: PC
"""
import json, requests, os
from datetime import datetime

from package.source import GetSource
from package.token import TokenSettings
from developer.package.norm_function import DATE_YMD_ONE, DATE_YMD_3TH
from developer.model.TForexQuotes import TForexQuotesField, TForexQuotesFormat

class BaseLogic:
    def __init__(self, obj):
        self.obj = obj

    def send_message(self, report: str='telegram', content_text: str='success'):
        match report:
            case 'line':
                url = 'https://notify-api.line.me/api/notify'
                headers = {'Authorization': 'Bearer ' + self.obj.line}
                data = {'message': content_text}
                res = requests.post(url, headers=headers, data=data)
            case 'telegram':
                url = (f'https://api.telegram.org/bot{self.obj.telegram[0]}/'
                       f'sendMessage?chat_id={self.obj.telegram[1]}&'
                       f'text={content_text}')
                res = requests.post(url)
            case _:
                pass

    def save_data(self, symbol: str, interval: str):
        self.obj.create_folder(f'datasets/{symbol.upper()}/{interval}')
        res = requests.get(GetSource.fmp(symbol, interval, self.obj.fmp))
        loader = json.loads(res.text)
        self.save_db(loader, symbol.upper(), interval)
        json.dump(loader, open(f'./datasets/{symbol.upper()}/{interval}/{symbol}_{str(datetime.now())[:10]}.json', 'w'))

    def save_db(self, loader: list, symbol: str, interval: str):
        datum = {}
        if isinstance(loader, list):
            for i in loader:
                try:
                    timestamp = datetime.strptime(i['date'], DATE_YMD_3TH).timestamp()
                    date = self.obj.trans_timestamp(timestamp, 46800)
                    key = f"{str(date)[:19]}_{symbol}_{interval}"
                    datum[key] = {
                        TForexQuotesField.CREATEDATETIME.value: date,
                        TForexQuotesField.SYMBOL.value: symbol,
                        TForexQuotesField.INTERVAL.value: interval,
                        TForexQuotesField.OPEN.value: self.obj.trans_decimal(i['open'], '0.01'),
                        TForexQuotesField.HIGH.value: self.obj.trans_decimal(i['high'], '0.01'),
                        TForexQuotesField.LOW.value: self.obj.trans_decimal(i['low'], '0.01'),
                        TForexQuotesField.CLOSE.value: self.obj.trans_decimal(i['close'], '0.01'),
                        TForexQuotesField.VOLUME.value: self.obj.trans_decimal(i['volume'], '0.01'),
                    }
                except:
                    self.obj.log_error('', exc_info=True)

        elif isinstance(loader, dict):
            for i in loader['historical']:
                try:
                    date = self.obj.trans_datetime(i['date'], DATE_YMD_ONE)
                    key = f"{str(date)[:19]}_{symbol}_{interval}"
                    datum[key] = {
                        TForexQuotesField.CREATEDATETIME.value: date,
                        TForexQuotesField.SYMBOL.value: symbol,
                        TForexQuotesField.INTERVAL.value: interval,
                        TForexQuotesField.OPEN.value: self.obj.trans_decimal(i['open'], '0.01'),
                        TForexQuotesField.HIGH.value: self.obj.trans_decimal(i['high'], '0.01'),
                        TForexQuotesField.LOW.value: self.obj.trans_decimal(i['low'], '0.01'),
                        TForexQuotesField.CLOSE.value: self.obj.trans_decimal(i['close'], '0.01'),
                        TForexQuotesField.VOLUME.value: self.obj.trans_decimal(i['volume'], '0.01'),
                    }
                except:
                    self.obj.log_error('', exc_info=True)
        else:
            raise ValueError('loader type error')

        self.obj.save_datum(db_name=TForexQuotesField.DB_NAME.value,
                            table_format=TForexQuotesFormat,
                            save_data=datum)