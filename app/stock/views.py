# -*- coding: utf-8 -*-

from flask import request
from flask import jsonify
import datetime
import numpy as np
from decimal import Decimal
from flask.views import View
from app.api.logics import BaoStockLogics

class StockView(View):
    def __init__(self):
        self.bao_stock = BaoStockLogics()

class InterestPeRatio(StockView):
    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        start_date = post_data.get('start_date', '2020-01-01')
        end_date = post_data.get('end_date', '')
        precision = post_data.get('precision', 0)
        precision = 0 if precision < 0 else precision
        status, message, price_list = self.calc_price_info(code, start_date, end_date, precision)
        result = {
          'code': 200 if status == '0' else status,
          'data': price_list,
          'msg': message
        }
        return jsonify(result)
    
    def calc_price_info(self, code, start_date, end_date, precision):
        attr_fields = ['high', 'low', 'close', 'peTTM']
        frequency = 'd'
        adjustflag = '3'
        current_year = datetime.datetime.now().year
        start_year = int(start_date.split('-')[0])
        price_list = []
        while start_year <= current_year:
            high = 0
            medium = 0
            low = 0
            peTTM = 0
            year = str(start_year)
            profit_fields = ['statDate', 'epsTTM', 'code']
            status, message, profit_list = self.bao_stock.query_profit_data(code=code, year=year, attr_fields=profit_fields, quarter='1')
            if status != '0':
                break
            start = year + '-01-01'
            end = year + '-12-31'
            status, message, data_list = self.bao_stock.query_history_k_data_plus(code=code, start_date=start, end_date=end, frequency=frequency, adjustflag=adjustflag, attr_fields=attr_fields)
            if status != '0':
                break
            precision_format = ('%.'+ str(precision) +'f') % 0
            highs = list(map(lambda x: Decimal(x['high']).quantize(Decimal(precision_format)), data_list))
            mediums = list(map(lambda x:  Decimal(x['close']).quantize(Decimal(precision_format)), data_list))
            lows = list(map(lambda x:  Decimal(x['low']).quantize(Decimal(precision_format)), data_list))
            peTTMs = list(map(lambda x:  Decimal(x['peTTM']).quantize(Decimal(precision_format)), data_list))
            high = np.max(highs).quantize(Decimal(precision_format))
            medium = np.median(mediums)
            low = np.min(lows).quantize(Decimal(precision_format))
            peTTM = np.mean(peTTMs).quantize(Decimal(precision_format))
            result = {
              "year": start_year,
              "high": str(high),
              "medium": str(medium),
              "low": str(low),
              "peTTM": str(peTTM),
              "epsTTM": profit_list
            }
            price_list.append(result)
            start_year += 1
        self.bao_stock.logout()
        return status, message, price_list
