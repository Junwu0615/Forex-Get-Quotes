# -*- coding: utf-8 -*-
from developer.utils.normal import *
from developer.modules.models.TForexQuotes import TForexQuotesField, TForexQuotesFormat

class UtilsLogic:
    def __init__(self, obj, logger):
        self.obj = obj
        self.logger = logger


    def fmp(self, item: str, key: str, token: str) -> str:
        start = '2000-01-01'
        end = '2060-01-01'
        base = 'https://financialmodelingprep.com/api/v3'
        fmp_resource = {
            # 'ALL': f"{base}/fx?apikey={token}",
            'M1': f"{base}/historical-chart/1min/{item.upper()}?from={start}&to={end}&apikey={token}",
            'M5': f"{base}/historical-chart/5min/{item.upper()}?from={start}&to={end}&apikey={token}",
            'M15': f"{base}/historical-chart/15min/{item.upper()}?from={start}&to={end}&apikey={token}",
            'H1': f"{base}/historical-chart/1hour/{item.upper()}?from={start}&to={end}&apikey={token}",
            'H4': f"{base}/historical-chart/4hour/{item.upper()}?from={start}&to={end}&apikey={token}",
            'D1': f"{base}/historical-price-full/{item.upper()}?apikey={token}",
            }
        return fmp_resource[key]


    def save_data(self, base_path: str, symbol: str, interval: str):
        try:
            os.makedirs(f'{base_path}/{symbol.upper()}/{interval}', exist_ok=True)
            res = requests.get(self.fmp(symbol, interval, self.obj.fmp))
            loader = json.loads(res.text)
            self.save_db(loader, symbol.upper(), interval)
            _save_f_name = f'{base_path}/{symbol.upper()}/{interval}/{symbol}_{str(datetime.now())[:10]}.json'
            json.dump(loader, open(_save_f_name, 'w'))

        except Exception as e:
            self.logger.error(exc_info=True)


    def save_db(self, loader: list, symbol: str, interval: str):
        datum = {}
        try:
            if isinstance(loader, list):
                for i in loader:
                    try:
                        timestamp = datetime.strptime(i['date'], LONG_FORMAT).timestamp()
                        date = trans_timestamp(timestamp, 46800)
                        key = f"{str(date)[:19]}_{symbol}_{interval}"
                        datum[key] = {
                            TForexQuotesField.CREATEDATETIME.value: date,
                            TForexQuotesField.SYMBOL.value: symbol,
                            TForexQuotesField.INTERVAL.value: interval,
                            TForexQuotesField.OPEN.value: trans_decimal(i['open'], '0.01'),
                            TForexQuotesField.HIGH.value: trans_decimal(i['high'], '0.01'),
                            TForexQuotesField.LOW.value: trans_decimal(i['low'], '0.01'),
                            TForexQuotesField.CLOSE.value: trans_decimal(i['close'], '0.01'),
                            TForexQuotesField.VOLUME.value: trans_decimal(i['volume'], '0.01'),
                        }
                    except Exception as e:
                        self.logger.error('', exc_info=True)

            elif isinstance(loader, dict):
                for i in loader['historical']:
                    try:
                        date = trans_datetime(i['date'], SHORT_FORMAT)
                        key = f"{str(date)[:19]}_{symbol}_{interval}"
                        datum[key] = {
                            TForexQuotesField.CREATEDATETIME.value: date,
                            TForexQuotesField.SYMBOL.value: symbol,
                            TForexQuotesField.INTERVAL.value: interval,
                            TForexQuotesField.OPEN.value: trans_decimal(i['open'], '0.01'),
                            TForexQuotesField.HIGH.value: trans_decimal(i['high'], '0.01'),
                            TForexQuotesField.LOW.value: trans_decimal(i['low'], '0.01'),
                            TForexQuotesField.CLOSE.value: trans_decimal(i['close'], '0.01'),
                            TForexQuotesField.VOLUME.value: trans_decimal(i['volume'], '0.01'),
                        }
                    except Exception as e:
                        self.logger.error('', exc_info=True)

            else:
                raise ValueError('loader type error')

            self.obj.save_datum(db_name=TForexQuotesField.DB_NAME.value,
                                table_format=TForexQuotesFormat,
                                save_data=datum)

        except Exception as e:
            self.logger.error(exc_info=True)