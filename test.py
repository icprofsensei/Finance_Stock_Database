import yfinance as yf
ticker_obj = yf.Ticker('AAPL')
allbalances = ticker_obj.balancesheet()
print(allbalances)