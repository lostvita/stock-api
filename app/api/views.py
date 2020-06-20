# -*- coding: utf-8 -*-

# from flask import Blueprint
from flask import request
from flask import jsonify
import datetime
from flask.views import View
from app.api.logics import BaoStockLogics


class ApiBase(View):
    def __init__(self):
        super().__init__()
        self.bao_stock = BaoStockLogics()

'''
@func: 获取历史A股K线数据
- code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- attr_fields：指示简称，支持多指标输入，以半角逗号分隔，填写内容作为返回类型的列。详细指标列表见历史行情指标参数章节，日线与分钟线参数不同。此参数不可为空；
- start_date：开始日期（包含），格式“YYYY-MM-DD”，为空时取2015-01-01；
- end_date：结束日期（包含），格式“YYYY-MM-DD”，为空时取最近一个交易日；
- frequency：数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写；指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
- adjustflag：复权类型，默认不复权：3；1：后复权；2：前复权。已支持分钟线、日线、周线、月线前后复权
'''
class QueryHistoryKDataPlus(ApiBase):
    def __init__(self):
        self.bao_stock = BaoStockLogics()

    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        start_date = post_data.get('start_date', '')
        end_date = post_data.get('end_date', '')
        frequency = post_data.get('frequency', 'd')
        adjustflag = post_data.get('adjustflag', '3')
        attr_fields = post_data.get('attr_fields', None)
        status, message, data_list = self.bao_stock.query_history_k_data_plus(code=code, start_date=start_date, end_date=end_date, attr_fields=attr_fields, frequency=frequency, adjustflag=adjustflag)
        result = {
          'code': 200 if status == '0' else status,
          'data': data_list,
          'msg': message
        }
        return jsonify(result)

'''
@func: 除权除息信息
- code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- year：年份，如：2017。此参数不可为空；
- yearType：年份类别，默认为"report":预案公告年份，可选项"operate":除权除息年份。此参数不可为空。
'''
class QueryDividendData(ApiBase):
    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        start_date = int(post_data.get('start_date', datetime.datetime.now().year))
        end_date = int(post_data.get('end_date', datetime.datetime.now().year))
        year_type = post_data.get('year_type', 'report')
        attr_fields = post_data.get('attr_fields', None)
        status, message, data_list = self.bao_stock.query_dividend_data(code=code, start_date=start_date, end_date=end_date, year_type=year_type, attr_fields=attr_fields)
        result = {
          'code': 200 if status == '0' else status,
          'data': data_list,
          'msg': message
        }
        return jsonify(result)


'''
@func: 获取季频盈利能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
- code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- year：统计年份，为空时默认当前年；
- quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
- attr_fields：过滤字段。取值范围：'code', 'pubDate', 'statDate', 'NRTurnRatio', 'NRTurnDays', 'INVTurnRatio', 'INVTurnDays', 'CATurnRatio', 'AssetTurnRatio'
'''
class QueryProfitData(ApiBase):
    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        year = post_data.get('year', datetime.datetime.now().year)
        attr_fields = post_data.get('attr_fields', None)
        quarter = post_data.get('quarter', '')
        status, message, profit_list = self.bao_stock.query_profit_data(code=code, year=year, quarter=quarter, attr_fields=attr_fields)       
        result = {
          'code': 200 if status == '0' else status,
          'data': profit_list,
          'msg': message
        }
        return jsonify(result)


'''
@func: 获取季频营运能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
- code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- year：统计年份，为空时默认当前年；
- quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
- attr_fields：过滤字段。取值范围：'code', 'pubDate', 'statDate', 'NRTurnRatio', 'NRTurnDays', 'INVTurnRatio', 'INVTurnDays', 'CATurnRatio', 'AssetTurnRatio'
'''
class QueryOperationData(ApiBase):
    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        year = post_data.get('year', datetime.datetime.now().year)
        attr_fields = post_data.get('attr_fields', None)
        quarter = post_data.get('quarter', '')
        status, message, operation_list = self.bao_stock.query_operation_data(code=code, year=year, quarter=quarter, attr_fields=attr_fields)
        result = {
          'code': 200 if status == '0' else status,
          'data': operation_list,
          'msg': message
        }
        return jsonify(result)


'''
@func: 获取季频成长能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
- code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- year：统计年份，为空时默认当前年；
- quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
- attr_fields：过滤字段。取值范围：'code', 'pubDate', 'statDate', 'YOYEquity', 'YOYAsset', 'YOYNI', 'YOYEPSBasic', 'YOYPNI'
'''
class QueryGrowthData(ApiBase):
    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        year = post_data.get('year', datetime.datetime.now().year)
        attr_fields = post_data.get('attr_fields', None)
        quarter = post_data.get('quarter', '')
        status, message, growth_list = self.bao_stock.query_growth_data(code=code, year=year, quarter=quarter, attr_fields=attr_fields)
        result = {
          'code': 200 if status == '0' else status,
          'data': growth_list,
          'msg': message
        }
        return jsonify(result)      


'''
@func: 获取季频偿债能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据
- code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- year：统计年份，为空时默认当前年；
- quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
- attr_fields：过滤字段。取值范围：'code', 'pubDate', 'statDate', 'currentRatio', 'quickRatio', 'cashRatio', 'YOYLiability', 'liabilityToAsset', 'assetToEquity'
'''
class QueryBalanceData(ApiBase):
    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        year = post_data.get('year', datetime.datetime.now().year)
        attr_fields = post_data.get('attr_fields', None)
        quarter = post_data.get('quarter', '')
        status, message, balance_list = self.bao_stock.query_balance_data(code=code, year=year, quarter=quarter, attr_fields=attr_fields)
        result = {
          'code': 200 if status == '0' else status,
          'data': balance_list,
          'msg': message
        }
        return jsonify(result)
        


'''
@func: 获取行业分类信息
- code：A股股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。可以为空；
- date：查询日期，格式XXXX-XX-XX，为空时默认最新日期。
- attr_fields：过滤字段。取值范围：['updateDate', 'code', 'code_name', 'industry', 'industryClassification']
'''
class QueryStockIndustry(ApiBase):
    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        date = post_data.get('date', '')
        attr_fields = post_data.get('attr_fields', None)
        status, message, industry_list = self.bao_stock.query_stock_industry(code=code, date=date, attr_fields=attr_fields)
        result = {
          'code': 200 if status == '0' else status,
          'data': industry_list,
          'msg': message
        }
        return jsonify(result)


'''
@func: 获取上证50成分股信息
- date：查询日期，格式XXXX-XX-XX，为空时默认最新日期
- attr_fields：过滤字段。取值范围：['updateDate', 'code', 'code_name']
'''
class QuerySz50Stocks(ApiBase):
    def dispatch_request(self):
        post_data = request.get_json()
        date = post_data.get('date', '')
        attr_fields = post_data.get('attr_fields', None)
        status, message, sz50_stocks = self.bao_stock.query_sz50_stocks(date=date, attr_fields=attr_fields)
        result = {
          'code': 200 if status == '0' else status,
          'data': sz50_stocks,
          'msg': message
        }
        return jsonify(result)

'''
@func: 获取沪深300成分股信息
- date：查询日期，格式XXXX-XX-XX，为空时默认最新日期
- attr_fields：过滤字段。取值范围：['updateDate', 'code', 'code_name']
'''
class QueryHs300Stocks(ApiBase):
    def dispatch_request(self):
        post_data = request.get_json()
        date = post_data.get('date', '')
        attr_fields = post_data.get('attr_fields', None)
        status, message, hs300_stocks = self.bao_stock.query_hs300_stocks(date=date, attr_fields=attr_fields)
        result = {
          'code': 200 if status == '0' else status,
          'data': hs300_stocks,
          'msg': message
        }
        return jsonify(result)


'''
@func: 获取中证500成分股信息
- date：查询日期，格式XXXX-XX-XX，为空时默认最新日期
- attr_fields：过滤字段。取值范围：['updateDate', 'code', 'code_name']
'''
class QueryZz500Stocks(ApiBase):
    def dispatch_request(self):
        post_data = request.get_json()
        date = post_data.get('date', '')
        attr_fields = post_data.get('attr_fields', None)
        status, message, zz500_stocks = self.bao_stock.query_zz500_stocks(date=date, attr_fields=attr_fields)
        result = {
          'code': 200 if status == '0' else status,
          'data': zz500_stocks,
          'msg': message
        }
        return jsonify(result)


'''
@func 获取证券基本资料
- code：A股股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。可以为空；
- code_name：股票名称，支持模糊查询，可以为空。
'''
class QueryStockBasic(ApiBase):
    def dispatch_request(self):
        post_data = request.get_json()
        code = post_data.get('code', '')
        code_name = post_data.get('code_name', '')
        attr_fields = post_data.get('attr_fields', None)
        status, message, data_list = self.bao_stock.query_stock_basic(code=code, code_name=code_name, attr_fields=attr_fields)
        result = {
          'code': 200 if status == '0' else status,
          'data': data_list,
          'msg': message
        }
        return jsonify(result)

