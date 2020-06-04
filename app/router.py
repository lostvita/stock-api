# from app.services.api import QueryHistoryKDataPlus
import app.services.api as StockView

def routes(app):
    # app.register_blueprint(BaoStock.mod)
    app.add_url_rule('/api/query_history_k_data_plus',view_func=StockView.QueryHistoryKDataPlus.as_view('query_history_k_data_plus'), methods=['POST'])
    app.add_url_rule('/api/query_dividend_data',view_func=StockView.QueryDividendData.as_view('query_dividend_data'), methods=['POST'])
    app.add_url_rule('/api/query_profit_data',view_func=StockView.QueryProfitData.as_view('query_profit_data'), methods=['POST'])
    app.add_url_rule('/api/query_operation_data',view_func=StockView.QueryOperationData.as_view('query_operation_data'), methods=['POST'])
    app.add_url_rule('/api/query_growth_data',view_func=StockView.QueryGrowthData.as_view('query_growth_data'), methods=['POST'])
    app.add_url_rule('/api/query_balance_data',view_func=StockView.QueryBalanceData.as_view('query_balance_data'), methods=['POST'])
    app.add_url_rule('/api/query_stock_industry',view_func=StockView.QueryStockIndustry.as_view('query_stock_industry'), methods=['POST'])
    app.add_url_rule('/api/query_sz50_stocks',view_func=StockView.QuerySz50Stocks.as_view('query_sz50_stocks'), methods=['POST'])
    app.add_url_rule('/api/query_hs300_stocks',view_func=StockView.QueryHs300Stocks.as_view('query_hs300_stocks'), methods=['POST'])
    app.add_url_rule('/api/query_zz500_stocks',view_func=StockView.QueryZz500Stocks.as_view('query_zz500_stocks'), methods=['POST'])