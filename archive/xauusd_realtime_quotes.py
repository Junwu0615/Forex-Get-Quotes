# -*- coding: utf-8 -*-
"""
@author: PC

FIXME
    Update Time: 2024-11-10
    程式邏輯須更新，寫法有異動 !
"""
import json, requests, time
from datetime import datetime
from package.token import TokenSettings
from schedule import every, run_pending, next_run

class RealtimeQuotes:
    def __init__(self):
        # Get Token
        token = token_settings()
        self.line_token, self.fmp_token = token.get_token()
        
        # Line Settings
        self.line_url = 'https://notify-api.line.me/api/notify'
        self.headers = { 'Authorization': 'Bearer ' + self.line_token}
        
        # Other Settings
        self.check_time = None
        while self.check_time is None:
            if datetime.now().time().minute % 5 == 0:
                self.check_time = datetime.now().timestamp()
        self.interval = 60*5 # Interval
        self.index = 1
        self.bool = False
    
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
        
    def save_data(self, key, save_path):
        res = requests.get(self.fmp_resource(self.fmp_token, key))
        kline = json.loads(res.text)
        json.dump(kline, open(save_path, 'w'))
    
    def main(self):
        self.send_message(f'Program Starting ... Time: {next_run()}')
        while True:
            if datetime.now().timestamp() > self.check_time+self.interval or self.index == 1:
                if '09:00' <= datetime.fromtimestamp(self.check_time).time().__str__() <= '24:00' \
                or '00:00' <= datetime.fromtimestamp(self.check_time).time().__str__() <= '04:00' :
                    try:
                        self.check_time = datetime.now().timestamp()
                        res = requests.get(self.fmp_resource(self.fmp_token, 'kline_m5'))
                        kline = json.loads(res.text)
                        if len(kline) != 0:
                            date = datetime.fromtimestamp(datetime.strptime(kline[0]['date'], '%Y-%m-%d %H:%M:%S').timestamp()+43200)
                            content_text = f"SendTime: {str(datetime.fromtimestamp(self.check_time))[11:19]}, "\
                                           f"Index: {self.index}, Time: {date}, O:{kline[0]['open']}, "\
                                           f"H:{kline[0]['high']}, L:{kline[0]['low']}, C:{kline[0]['close']}."
                                           
                            self.send_message(content_text)
                            print(content_text)
                        self.bool = True
                        self.index += 1
                        
                    except IOError as e:
                        self.send_message('Error Type: <except>')
                        print(e)
                        
                elif self.index != 1 and self.bool:
                    self.save_data('kline_m5', f'./History_KLine_M5/xauusd_{str(datetime.now())[:10]}.json')
                    self.save_data('kline_d1', f'./History_KLine_D1/xauusd_{str(datetime.now())[:10]}.json')
                    self.send_message('Program ShutDown ...')
                    break

                else:
                    self.check_time = datetime.now().timestamp()
                    time.sleep(1)
            
def doto_main():
    quotes = realtime_quotes()
    quotes.main()
    
def check_schedule(do_time):
    every().monday.at(do_time).do(doto_main)      # 星期一
    every().tuesday.at(do_time).do(doto_main)     # 星期二
    every().wednesday.at(do_time).do(doto_main)   # 星期三
    every().thursday.at(do_time).do(doto_main)    # 星期四
    every().friday.at(do_time).do(doto_main)      # 星期五
    #every().saturday.at(do_time).do(doto_main)    # 星期六
    #every().sunday.at(do_time).do(doto_main)      # 星期天
                 
if __name__ == "__main__":
    check_schedule(do_time='08:55:00')
    while True:
        run_pending()
        time.sleep(1)
