import yfinance as yf
ticker_obj = yf.Ticker('SEDG')
allbalances = ticker_obj.balancesheet
print(allbalances)