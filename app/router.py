import app.api.views as ApiView
import app.stock.views as StockView

def routes(app):
    # app.register_blueprint(BaoStock.mod)
    app.add_url_rule('/api/query_history_k_data_plus',view_func=ApiView.QueryHistoryKDataPlus.as_view('query_history_k_data_plus'), methods=['POST'])
    app.add_url_rule('/api/query_dividend_data',view_func=ApiView.QueryDividendData.as_view('query_dividend_data'), methods=['POST'])
    app.add_url_rule('/api/query_profit_data',view_func=ApiView.QueryProfitData.as_view('query_profit_data'), methods=['POST'])
    app.add_url_rule('/api/query_operation_data',view_func=ApiView.QueryOperationData.as_view('query_operation_data'), methods=['POST'])
    app.add_url_rule('/api/query_growth_data',view_func=ApiView.QueryGrowthData.as_view('query_growth_data'), methods=['POST'])
    app.add_url_rule('/api/query_balance_data',view_func=ApiView.QueryBalanceData.as_view('query_balance_data'), methods=['POST'])
    app.add_url_rule('/api/query_stock_industry',view_func=ApiView.QueryStockIndustry.as_view('query_stock_industry'), methods=['POST'])
    app.add_url_rule('/api/query_sz50_stocks',view_func=ApiView.QuerySz50Stocks.as_view('query_sz50_stocks'), methods=['POST'])
    app.add_url_rule('/api/query_hs300_stocks',view_func=ApiView.QueryHs300Stocks.as_view('query_hs300_stocks'), methods=['POST'])
    app.add_url_rule('/api/query_zz500_stocks',view_func=ApiView.QueryZz500Stocks.as_view('query_zz500_stocks'), methods=['POST'])
    app.add_url_rule('/api/query_stock_basic',view_func=ApiView.QueryStockBasic.as_view('query_stock_basic'), methods=['POST'])

    app.add_url_rule('/stock/interest_pe_ratio',view_func=StockView.InterestPeRatio.as_view('interest_pe_ratio'), methods=['POST'])
    # app.add_url_rule('/stock/interest_pe_ratio',view_func=StockView.InterestPeRatio.as_view('interest_pe_ratio'), methods=['POST'])

