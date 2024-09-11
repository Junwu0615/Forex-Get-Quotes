# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:56:52 2024
@author: PC
"""
import json, requests
# from bs4 import BeautifulSoup
from datetime import datetime
from token_settings import token_settings

class realtime_quotes:
    
    def __init__(self):
        # Get Token
        token = token_settings()
        self.line_token, self.fmp_token = token.get_token()
        
        # Line Settings
        self.line_url = 'https://notify-api.line.me/api/notify'
        self.headers = { 'Authorization': 'Bearer ' + self.line_token}
        
        # Other Settings
        self.check_time = datetime.now().timestamp()
        self.index = 1
        self.interval = 60*5 # Interval
        self.bool = True
    
    def fmp_resource(self, token, key):
        fmp_resource = {
            'all_quotes': f"https://financialmodelingprep.com/api/v3/fx?apikey={token}",
            'kline_m5': f"https://financialmodelingprep.com/api/v3/historical-chart/5min/XAUUSD?from=2000-01-01&to=2030-01-01&apikey={token}",
            'kline_d1': f"https://financialmodelingprep.com/api/v3/historical-price-full/XAUUSD?apikey={token}",
            }
        return fmp_resource[key]
    
    def send_message(self, content_text):
        data = {'message': content_text}
        data = requests.post(self.line_url, headers=self.headers, data=data)
    
    def main(self):
        self.send_message('Program Starting ...')
        while True:
            if datetime.now().timestamp() > self.check_time+self.interval:
                if '09:00' < datetime.fromtimestamp(self.check_time).time().__str__() < '24:00' \
                or '00:00' < datetime.fromtimestamp(self.check_time).time().__str__() < '04:00' :
                    try:
                        res = requests.get(self.fmp_resource(self.fmp_token, 'kline_m5'))
                        kline = json.loads(res.text)
                        if len(kline) != 0:
                            #content_text = f"Index: {self.index}, Time: {xauusd['date']}, "\
                            #               f"Bid:{xauusd['bid']}, Ask:{xauusd['ask']}, Changes:{xauusd['changes']}, "\
                            #               f"O:{xauusd['open']}, H:{xauusd['high']}, L:{xauusd['low']}."
                            
                            content_text = f"Index: {self.index}, Time: {kline[0]['date']}, O:{kline[0]['open']}, "\
                                           f"H:{kline[0]['high']}, L:{kline[0]['low']}, C:{kline[0]['close']}."
                                           
                            self.send_message(content_text)
                            print(content_text)
                        self.check_time = datetime.now().timestamp()
                        self.index += 1
                        self.bool = True
                        
                    except IOError as e:
                        self.send_message('Error Type: <except>')
                        print(e)
                else:
                    if self.bool:
                        res = requests.get(self.fmp_resource(self.fmp_token, 'kline_m5'))
                        kline = json.loads(res.text)
                        json.dump(kline, open(f'./History_KLine_M5/xauusd_{str(datetime.now())[:10]}.json', 'w'))
                        
                        res = requests.get(self.fmp_resource(self.fmp_token, 'kline_d1'))
                        kline = json.loads(res.text)
                        json.dump(kline, open(f'./History_KLine_D1/xauusd_{str(datetime.now())[:10]}.json', 'w'))
                        
                        self.send_message('Program ShutDown ...')
                        self.bool = False
                        
                    self.check_time = datetime.now().timestamp()
                    self.index = 1
                                     
if __name__ == "__main__":
    quotes = realtime_quotes()
    quotes.main()