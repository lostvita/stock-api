# -*- coding: utf-8 -*-

# from flask import Blueprint
from flask import request
from flask import jsonify
import datetime
from flask.views import View
import baostock as bs
from app.utils.index import jsonWrapper

class BaoStockView(View):
    def __init__(self):
        super().__init__()
        lg = bs.login()

    def logout(self):
        bs.logout()


'''
@func: 获取历史A股K线数据
- code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- fields：指示简称，支持多指标输入，以半角逗号分隔，填写内容作为返回类型的列。详细指标列表见历史行情指标参数章节，日线与分钟线参数不同。此参数不可为空；
- start：开始日期（包含），格式“YYYY-MM-DD”，为空时取2015-01-01；
- end：结束日期（包含），格式“YYYY-MM-DD”，为空时取最近一个交易日；
- frequency：数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写；指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
- adjustflag：复权类型，默认不复权：3；1：后复权；2：前复权。已支持分钟线、日线、周线、月线前后复权
'''
class QueryHistoryKDataPlus(BaoStockView):
    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        start_date = post_data.get('start_date', '')
        end_date = post_data.get('end_date', '')
        frequency = post_data.get('frequency', 'd')
        adjustflag = post_data.get('adjustflag', '3')
        attr_fields = post_data.get('attr_fields', ['date','code','open','high','low','close','preclose','volume','amount','adjustflag','turn','tradestatus','pctChg','isST'])
        rs = bs.query_history_k_data_plus(code, ','.join(attr_fields), start_date=start_date, end_date=end_date, frequency=frequency, adjustflag=adjustflag)
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = {
          'code': 200 if rs.error_code == '0' else rs.error_code,
          'data': jsonWrapper(data_list, attr_fields),
          'msg': rs.error_msg
        }
        self.logout()
        return jsonify(result)


'''
@func: 除权除息信息
- code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- year：年份，如：2017。此参数不可为空；
- yearType：年份类别，默认为"report":预案公告年份，可选项"operate":除权除息年份。此参数不可为空。
'''
class QueryDividendData(BaoStockView):
    def dispatch_request(self):
        post_data = request.get_json()
        self.code = post_data.get('code', '')
        start_date = int(post_data.get('start_date', datetime.datetime.now().year))
        end_date = int(post_data.get('end_date', datetime.datetime.now().year))
        self.year_type = post_data.get('year_type', 'report')
        self.attr_fields = post_data.get('attr_fields', None)
        error_code = '0'
        error_msg = 'success'
        data_list = []
        while start_date <= end_date:
            error_code, error_msg, data = self.query_dividend_data(start_date)
            if error_code != '0':
                break
            data_list.append({
              'date': start_date,
              'data': data
            })
            start_date += 1
        result = {
          'code': 200 if error_code == '0' else error_code,
          'data': data_list,
          'msg': error_msg
        }
        self.logout()
        return jsonify(result)
      
    def query_dividend_data(self, year):
        data_list = []
        fields = ['code', 'dividPreNoticeDate', 'dividAgmPumDate', 'dividPlanAnnounceDate', 'dividPlanDate', 'dividRegistDate', 'dividOperateDate', 'dividPayDate', 'dividStockMarketDate', 'dividCashPsBeforeTax', 'dividCashPsAfterTax', 'dividStocksPs', 'dividCashStock', 'dividReserveToStockPs']
        rs = bs.query_dividend_data(self.code, year, yearType=self.year_type)
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        data = jsonWrapper(data_list, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in self.attr_fields }, data)) if self.attr_fields else data


'''
@func: 获取季频盈利能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
- code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- year：统计年份，为空时默认当前年；
- quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
- attr_fields：过滤字段。取值范围：'code', 'pubDate', 'statDate', 'NRTurnRatio', 'NRTurnDays', 'INVTurnRatio', 'INVTurnDays', 'CATurnRatio', 'AssetTurnRatio'
'''
class QueryProfitData(BaoStockView):
    def dispatch_request(self):
        post_data = request.get_json()
        self.code = post_data.get('code', '')
        self.year = post_data.get('year', datetime.datetime.now().year)
        self.attr_fields = post_data.get('attr_fields', None)
        quarter = post_data.get('quarter', '')
        error_code = '0'
        error_msg = 'success'
        profit_list = []
        if quarter:
            error_code, error_msg, data = self.query_profit_data(quarter)
            profit_list = data
        else:
            quarter = 1
            while quarter <= 4:
                error_code, error_msg, data = self.query_profit_data(quarter)
                if error_code != '0':
                  break
                profit_list.append(data[0] if len(data) == 1 else {})
                quarter += 1
                
        result = {
          'code': 200 if error_code == '0' else error_code,
          'data': profit_list,
          'msg': error_msg
        }
        self.logout()
        return jsonify(result)
        
    
    def query_profit_data(self, quarter):
        data_list = []
        rs = bs.query_profit_data(code=self.code, year=self.year, quarter=quarter)
        fields = ['code', 'pubDate', 'statDate', 'roeAvg', 'npMargin', 'gpMargin', 'netProfit', 'epsTTM', 'MBRevenue', 'totalShare', 'liqaShare']
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        data = jsonWrapper(data_list, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in self.attr_fields }, data)) if self.attr_fields else data

'''
@func: 获取季频营运能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
- code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- year：统计年份，为空时默认当前年；
- quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
- attr_fields：过滤字段。取值范围：'code', 'pubDate', 'statDate', 'NRTurnRatio', 'NRTurnDays', 'INVTurnRatio', 'INVTurnDays', 'CATurnRatio', 'AssetTurnRatio'
'''
class QueryOperationData(BaoStockView):
    def dispatch_request(self):
        post_data = request.get_json()
        self.code = post_data.get('code', '')
        self.year = post_data.get('year', datetime.datetime.now().year)
        self.attr_fields = post_data.get('attr_fields', None)
        quarter = post_data.get('quarter', '')
        error_code = '0'
        error_msg = 'success'
        operation_list = []
        if quarter:
            error_code, error_msg, data = self.query_operation_data(quarter)
            operation_list = data
        else:
            quarter = 1
            while quarter <= 4:
                error_code, error_msg, data = self.query_operation_data(quarter)
                if error_code != '0':
                  break
                operation_list.append(data[0] if len(data) == 1 else {})
                quarter += 1
                
        result = {
          'code': 200 if error_code == '0' else error_code,
          'data': operation_list,
          'msg': error_msg
        }
        self.logout()
        return jsonify(result)
    
    def query_operation_data(self, quarter):
        data_list = []
        rs = bs.query_operation_data(code=self.code, year=self.year, quarter=quarter)
        fields = ['code', 'pubDate', 'statDate', 'NRTurnRatio', 'NRTurnDays', 'INVTurnRatio', 'INVTurnDays', 'CATurnRatio', 'AssetTurnRatio']
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        data = jsonWrapper(data_list, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in self.attr_fields }, data)) if self.attr_fields else data


'''
@func: 获取季频成长能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
- code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- year：统计年份，为空时默认当前年；
- quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
- attr_fields：过滤字段。取值范围：'code', 'pubDate', 'statDate', 'YOYEquity', 'YOYAsset', 'YOYNI', 'YOYEPSBasic', 'YOYPNI'
'''
class QueryGrowthData(BaoStockView):
    def dispatch_request(self):
        post_data = request.get_json()
        self.code = post_data.get('code', '')
        self.year = post_data.get('year', datetime.datetime.now().year)
        self.attr_fields = post_data.get('attr_fields', None)
        quarter = post_data.get('quarter', '')
        error_code = '0'
        error_msg = 'success'
        growth_list = []
        if quarter:
            error_code, error_msg, data = self.query_growth_data(quarter)
            growth_list = data
        else:
            quarter = 1
            while quarter <= 4:
                error_code, error_msg, data = self.query_growth_data(quarter)
                if error_code != '0':
                  break
                growth_list.append(data[0] if len(data) == 1 else {})
                quarter += 1
                
        result = {
          'code': 200 if error_code == '0' else error_code,
          'data': growth_list,
          'msg': error_msg
        }
        self.logout()
        return jsonify(result)
    
    def query_growth_data(self, quarter):
        data_list = []
        rs = bs.query_growth_data(code=self.code, year=self.year, quarter=quarter)
        fields = ['code', 'pubDate', 'statDate', 'YOYEquity', 'YOYAsset', 'YOYNI', 'YOYEPSBasic', 'YOYPNI']
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        data = jsonWrapper(data_list, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in self.attr_fields }, data)) if self.attr_fields else data


'''
@func: 获取季频偿债能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
- code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- year：统计年份，为空时默认当前年；
- quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
- attr_fields：过滤字段。取值范围：'code', 'pubDate', 'statDate', 'currentRatio', 'quickRatio', 'cashRatio', 'YOYLiability', 'liabilityToAsset', 'assetToEquity'
'''
class QueryBalanceData(BaoStockView):
    def dispatch_request(self):
        post_data = request.get_json()
        self.code = post_data.get('code', '')
        self.year = post_data.get('year', datetime.datetime.now().year)
        self.attr_fields = post_data.get('attr_fields', None)
        quarter = post_data.get('quarter', '')
        error_code = '0'
        error_msg = 'success'
        balance_list = []
        if quarter:
            error_code, error_msg, data = self.query_balance_data(quarter)
            balance_list = data
        else:
            quarter = 1
            while quarter <= 4:
                error_code, error_msg, data = self.query_balance_data(quarter)
                if error_code != '0':
                  break
                balance_list.append(data[0] if len(data) == 1 else {})
                quarter += 1
                
        result = {
          'code': 200 if error_code == '0' else error_code,
          'data': balance_list,
          'msg': error_msg
        }
        self.logout()
        return jsonify(result)
    
    def query_balance_data(self, quarter):
        data_list = []
        rs = bs.query_balance_data(code=self.code, year=self.year, quarter=quarter)
        fields = ['code', 'pubDate', 'statDate', 'currentRatio', 'quickRatio', 'cashRatio', 'YOYLiability', 'liabilityToAsset', 'assetToEquity']
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        data = jsonWrapper(data_list, fields)
        return rs.error_code, rs.error_msg, list(map(lambda x: { attr: x.get(attr, '') for attr in self.attr_fields }, data)) if self.attr_fields else data


'''
@func: 获取行业分类信息
- code：A股股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。可以为空；
- date：查询日期，格式XXXX-XX-XX，为空时默认最新日期。
- attr_fields：过滤字段。取值范围：['updateDate', 'code', 'code_name', 'industry', 'industryClassification']
'''
class QueryStockIndustry(BaoStockView):
    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        date = post_data.get('date', '')
        attr_fields = post_data.get('attr_fields', None)
        rs = bs.query_stock_industry(code=code, date=date)
        industry_list = []
        while (rs.error_code == '0') & rs.next():
            industry_list.append(rs.get_row_data())
        fields = ['updateDate', 'code', 'code_name', 'industry', 'industryClassification']
        data = jsonWrapper(industry_list, fields)
        result = {
          'code': 200 if rs.error_code == '0' else rs.error_code,
          'data': list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data,
          'msg': rs.error_msg
        }
        self.logout()
        return jsonify(result)


'''
@func: 获取上证50成分股信息
- date：查询日期，格式XXXX-XX-XX，为空时默认最新日期
- attr_fields：过滤字段。取值范围：['updateDate', 'code', 'code_name']
'''
class QuerySz50Stocks(BaoStockView):
    def dispatch_request(self):
        post_data = request.get_json()
        date = post_data.get('date', '')
        attr_fields = post_data.get('attr_fields', None)
        rs = bs.query_sz50_stocks(date=date)
        sz50_stocks = []
        while (rs.error_code == '0') & rs.next():
          sz50_stocks.append(rs.get_row_data())
        fields = ['updateDate', 'code', 'code_name']
        data = jsonWrapper(sz50_stocks, fields)
        result = {
          'code': 200 if rs.error_code == '0' else rs.error_code,
          'data': list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data,
          'msg': rs.error_msg
        }
        self.logout()
        return jsonify(result)

'''
@func: 获取沪深300成分股信息
- date：查询日期，格式XXXX-XX-XX，为空时默认最新日期
- attr_fields：过滤字段。取值范围：['updateDate', 'code', 'code_name']
'''
class QueryHs300Stocks(BaoStockView):
    def dispatch_request(self):
        post_data = request.get_json()
        date = post_data.get('date', '')
        attr_fields = post_data.get('attr_fields', None)
        rs = bs.query_hs300_stocks(date=date)
        hs50_stocks = []
        while (rs.error_code == '0') & rs.next():
          hs50_stocks.append(rs.get_row_data())
        fields = ['updateDate', 'code', 'code_name']
        data = jsonWrapper(hs50_stocks, fields)
        result = {
          'code': 200 if rs.error_code == '0' else rs.error_code,
          'data': list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data,
          'msg': rs.error_msg
        }
        self.logout()
        return jsonify(result)


'''
@func: 获取中证500成分股信息
- date：查询日期，格式XXXX-XX-XX，为空时默认最新日期
- attr_fields：过滤字段。取值范围：['updateDate', 'code', 'code_name']
'''
class QueryZz500Stocks(BaoStockView):
    def dispatch_request(self):
        post_data = request.get_json()
        date = post_data.get('date', '')
        attr_fields = post_data.get('attr_fields', None)
        rs = bs.query_zz500_stocks(date=date)
        zz500_stocks = []
        while (rs.error_code == '0') & rs.next():
          zz500_stocks.append(rs.get_row_data())
        fields = ['updateDate', 'code', 'code_name']
        data = jsonWrapper(zz500_stocks, fields)
        result = {
          'code': 200 if rs.error_code == '0' else rs.error_code,
          'data': list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data,
          'msg': rs.error_msg
        }
        self.logout()
        return jsonify(result)


'''
@func 获取证券基本资料
- code：A股股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。可以为空；
- code_name：股票名称，支持模糊查询，可以为空。
'''
class QueryStockBasic(BaoStockView):
    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        code_name = post_data.get('code_name', '')
        attr_fields = post_data.get('attr_fields', None)
        rs = bs.query_stock_basic(code=code, code_name=code_name)
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        fields = ['code', 'code_name', 'ipoDate', 'outDate', 'type', 'status']
        data = jsonWrapper(data_list, fields)
        result = {
          'code': 200 if rs.error_code == '0' else rs.error_code,
          'data': list(map(lambda x: { attr: x.get(attr, '') for attr in attr_fields }, data)) if attr_fields else data,
          'msg': rs.error_msg
        }
        self.logout()
        return jsonify(result)
