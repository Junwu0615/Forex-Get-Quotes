# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 00:03:07 2024

@author: PC
"""
class GetSource:
    @staticmethod
    def fmp(item: str, key: str, token: str) -> str:
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