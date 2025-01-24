# -*- coding: utf-8 -*-
class TokenSettings:
    @staticmethod
    def get_token(todo: str):
        for idx in [i for i in open('package/token.txt', 'r')]:
            idx_ = idx.split(',')
            if idx_[0] == todo:
                match todo:
                    case 'LINE':
                        return idx_[1].replace('\n','')
                    case 'FMP':
                        return idx_[1].replace('\n','')
                    case 'TELEGRAM':
                        return [idx_[1].replace('\n',''),
                                idx_[2].replace('\n','')]
                    case _:
                        pass

    @staticmethod
    def line() -> str:
        return TokenSettings.get_token('LINE')

    @staticmethod
    def fmp() -> str:
        return TokenSettings.get_token('FMP')

    @staticmethod
    def telegram() -> str:
        return TokenSettings.get_token('TELEGRAM')