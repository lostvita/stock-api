# -*- coding: utf-8 -*-

import baostock as bs
from app.utils.index import jsonWrapper

class BaoStockBase():
    def __init__(self):
        super().__init__()
        lg = bs.login()

    def logout(self):
        bs.logout()

class BaoStockLogics(BaoStockBase):
    def query_history_k_data_plus(self, code, start_date, end_date, attr_fields, frequency, adjustflag):
      fields = ['date','code','open','high','low','close','preclose','volume','amount','adjustflag','turn','tradestatus','pctChg', 'peTTM', 'pbMRQ', 'psTTM', 'pcfNcfTTM', 'isST']
      if attr_fields:
          attr_fields = list(filter(lambda x: x in fields, attr_fields))
      else: 
          attr_fields = fields
      rs = bs.query_history_k_data_plus(code, ','.join(attr_fields), start_date=start_date, end_date=end_date, frequency=frequency, adjustflag=adjustflag)
      data_list = []
      while (rs.error_code == '0') & rs.next():
          data_list.append(rs.get_row_data())
      self.logout()
      return rs.error_code, rs.error_msg, jsonWrapper(data_list, attr_fields)

    def query_dividend_data(self, code, start_date, end_date, year_type, attr_fields):
        error_code = '0'
        error_msg = 'success'
        data_list = []
        while start_date <= end_date:
            error_code, error_msg, data = self.do_query_dividend_data(year=start_date, code=code, year_type=year_type, attr_fields=attr_fields)
            if error_code != '0':
                break
            data_list.append({
              'date': start_date,
              'data': data
            })
            start_date += 1
        return error_code, error_msg, data_list
    
    def do_query_dividend_data(self, year, code, year_type, attr_fields):
        data_list = []
        fields = ['code', 'dividPreNoticeDate', 'dividAgmPumDate', 'dividPlanAnnounceDate', 'dividPlanDate', 'dividRegistDate', 'dividOperateDate', 'dividPayDate', 'dividStockMarketDate', 'dividCashPsBeforeTax', 'dividCashPsAfterTax', 'dividStocksPs', 'dividCashStock', 'dividReserveToStockPs']
        rs = bs.query_dividend_data(code, year, yearType=year_type)
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        data = jsonWrapper(data_list, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data

    def query_profit_data(self, code, year, quarter, attr_fields):
        error_code = '0'
        error_msg = 'success'
        profit_list = []
        if quarter:
            error_code, error_msg, data = self.do_query_profit_data(code=code, year=year, quarter=quarter, attr_fields=attr_fields)
            profit_list = data
        else:
            quarter = 1
            while quarter <= 4:
                error_code, error_msg, data = self.do_query_profit_data(code=code, year=year, quarter=quarter, attr_fields=attr_fields)
                if error_code != '0':
                  break
                profit_list.append(data[0] if len(data) == 1 else {})
                quarter += 1
        return error_code, error_msg, profit_list
    
    def do_query_profit_data(self, code, year, quarter, attr_fields):
        data_list = []
        rs = bs.query_profit_data(code=code, year=year, quarter=quarter)
        fields = ['code', 'pubDate', 'statDate', 'roeAvg', 'npMargin', 'gpMargin', 'netProfit', 'epsTTM', 'MBRevenue', 'totalShare', 'liqaShare']
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        data = jsonWrapper(data_list, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data
    
    def query_operation_data(self, code, year, quarter, attr_fields):
        error_code = '0'
        error_msg = 'success'
        operation_list = []
        if quarter:
            error_code, error_msg, data = self.do_query_operation_data(code=code, year=year, quarter=quarter, attr_fields=attr_fields)
            operation_list = data
        else:
            quarter = 1
            while quarter <= 4:
                error_code, error_msg, data = self.do_query_operation_data(code=code, year=year, quarter=quarter, attr_fields=attr_fields)
                if error_code != '0':
                  break
                operation_list.append(data[0] if len(data) == 1 else {})
                quarter += 1
        return error_code, error_msg, operation_list
    
    def do_query_operation_data(self, code, year, quarter, attr_fields):
        data_list = []
        rs = bs.query_operation_data(code=code, year=year, quarter=quarter)
        fields = ['code', 'pubDate', 'statDate', 'NRTurnRatio', 'NRTurnDays', 'INVTurnRatio', 'INVTurnDays', 'CATurnRatio', 'AssetTurnRatio']
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        data = jsonWrapper(data_list, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data

    def query_growth_data(self, code, year, quarter, attr_fields):
        error_code = '0'
        error_msg = 'success'
        growth_list = []
        if quarter:
            error_code, error_msg, data = self.do_query_growth_data(code=code, year=year, quarter=quarter, attr_fields=attr_fields)
            growth_list = data
        else:
            quarter = 1
            while quarter <= 4:
                error_code, error_msg, data = self.do_query_growth_data(code=code, year=year, quarter=quarter, attr_fields=attr_fields)
                if error_code != '0':
                  break
                growth_list.append(data[0] if len(data) == 1 else {})
                quarter += 1
        return error_code, error_msg, growth_list
    
    def do_query_growth_data(self, code, year, quarter, attr_fields):
        data_list = []
        rs = bs.query_growth_data(code=code, year=year, quarter=quarter)
        fields = ['code', 'pubDate', 'statDate', 'YOYEquity', 'YOYAsset', 'YOYNI', 'YOYEPSBasic', 'YOYPNI']
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        data = jsonWrapper(data_list, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data

    def query_balance_data(self, code, year, quarter, attr_fields):
        error_code = '0'
        error_msg = 'success'
        balance_list = []
        if quarter:
            error_code, error_msg, data = self.do_query_balance_data(code=code, year=year, quarter=quarter, attr_fields=attr_fields)
            balance_list = data
        else:
            quarter = 1
            while quarter <= 4:
                error_code, error_msg, data = self.do_query_balance_data(code=code, year=year, quarter=quarter, attr_fields=attr_fields)
                if error_code != '0':
                  break
                balance_list.append(data[0] if len(data) == 1 else {})
                quarter += 1
        return error_code, error_msg, balance_list
    
    def do_query_balance_data(self, code, year, quarter, attr_fields):
        data_list = []
        rs = bs.query_balance_data(code=code, year=year, quarter=quarter)
        fields = ['code', 'pubDate', 'statDate', 'currentRatio', 'quickRatio', 'cashRatio', 'YOYLiability', 'liabilityToAsset', 'assetToEquity']
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        data = jsonWrapper(data_list, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data
    
    def query_stock_industry(self, code, date, attr_fields):
        rs = bs.query_stock_industry(code=code, date=date)
        industry_list = []
        while (rs.error_code == '0') & rs.next():
            industry_list.append(rs.get_row_data())
        fields = ['updateDate', 'code', 'code_name', 'industry', 'industryClassification']
        data = jsonWrapper(industry_list, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data
    
    def query_sz50_stocks(self, date, attr_fields):
        rs = bs.query_sz50_stocks(date=date)
        sz50_stocks = []
        while (rs.error_code == '0') & rs.next():
          sz50_stocks.append(rs.get_row_data())
        fields = ['updateDate', 'code', 'code_name']
        data = jsonWrapper(sz50_stocks, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data
    
    def query_hs300_stocks(self, date, attr_fields):
        rs = bs.query_hs300_stocks(date=date)
        hs300_stocks = []
        while (rs.error_code == '0') & rs.next():
          hs300_stocks.append(rs.get_row_data())
        fields = ['updateDate', 'code', 'code_name']
        data = jsonWrapper(hs300_stocks, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data
    
    def query_zz500_stocks(self, date, attr_fields):
        rs = bs.query_zz500_stocks(date=date)
        zz500_stocks = []
        while (rs.error_code == '0') & rs.next():
          zz500_stocks.append(rs.get_row_data())
        fields = ['updateDate', 'code', 'code_name']
        data = jsonWrapper(zz500_stocks, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data

    def query_stock_basic(self, code, code_name, attr_fields):
        rs = bs.query_stock_basic(code=code, code_name=code_name)
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        fields = ['code', 'code_name', 'ipoDate', 'outDate', 'type', 'status']
        data = jsonWrapper(data_list, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data

