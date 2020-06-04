# from app.services.api import QueryHistoryKDataPlus
import app.services.api as StockView

def routes(app):
    # app.register_blueprint(BaoStock.mod)
    app.add_url_rule('/api/query_history_k_data_plus',view_func=StockView.QueryHistoryKDataPlus.as_view('query_history_k_data_plus'), methods=['POST'])
    app.add_url_rule('/api/query_dividend_data',view_func=StockView.QueryDividendData.as_view('query_dividend_data'), methods=['POST'])
    app.add_url_rule('/api/query_profit_data',view_func=StockView.QueryProfitData.as_view('query_profit_data'), methods=['POST'])
    app.add_url_rule('/api/query_operation_data',view_func=StockView.QueryOperationData.as_view('query_operation_data'), methods=['POST'])