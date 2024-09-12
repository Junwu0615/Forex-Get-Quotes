# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 00:03:07 2024

@author: PC
"""
import json, requests, os
from datetime import datetime

from package.source import GetSource
from package.token import TokenSettings

class BaseLogic:
    def __init__(self, obj):
        self.obj = obj

    def send_message(self, key: str='telegram', content_text: str='success'):
        match key:
            case 'line':
                url = 'https://notify-api.line.me/api/notify'
                headers = {'Authorization': 'Bearer ' + self.obj.line}
                data = {'message': content_text}
                res = requests.post(url, headers=headers, data=data)
            case 'telegram':
                url = (f'https://api.telegram.org/bot{self.obj.elegram[0]}/'
                       f'sendMessage?chat_id={self.obj.telegram[1]}&'
                       f'text={content_text}')
                res = requests.post(url)
            case _:
                pass

    def save_in_json(self, item: str, key: str):
        self.obj.create_folder(f'datasets/{item.upper()}/{key}')
        res = requests.get(GetSource.fmp(item, key, self.obj.fmp))
        kline = json.loads(res.text)
        json.dump(kline, open(f'./datasets/{item.upper()}/{key}/{item}_{str(datetime.now())[:10]}.json', 'w'))

    def save_in_db(self):
        pass