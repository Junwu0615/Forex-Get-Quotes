# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 00:03:07 2024

@author: PC
"""
class TokenSettings:
    @staticmethod
    def get_token(todo: str):
        for idx in [i for i in open('package/token.txt', 'r')]:
            idx_ = idx.split(',')
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
        return TokenSettings.get_token('LINE')

    @staticmethod
    def telegram() -> str:
        return TokenSettings.get_token('LINE')