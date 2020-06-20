# -*- coding: utf-8 -*-

from flask import request
from flask import jsonify
import datetime
from flask.views import View
from app.api.logics import BaoStockLogics

class InterestPeRatio(View):
    def __init__(self):
        self.bao_stock = BaoStockLogics()

    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        status = 0
        message = 'success'
        data_list = [code]
        result = {
          'code': 200 if status == '0' else status,
          'data': data_list,
          'msg': message
        }
        return jsonify(result)
