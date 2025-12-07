import yfinance as yf
ticker_obj = yf.Ticker('SEDG')
'''allbalances = ticker_obj.balancesheet
allearnings = ticker_obj.earnings_history
allcash = ticker_obj.cash_flow'''
quarterlyreports = ticker_obj.get_balance_sheet()
print(quarterlyreports)