import yfinance as yf

symbols = {
    "BMO Low Volatility Canadian Equity ETF":'ZLB.TO', 
    "Vanguard FTSE Canadian High Dividend Yield Index ETF": 'VDY.TO',
    "BMO MSCI All Country World High Quality Index ETF": 'ZGQ.TO'}


for etf_name,sym in symbols.items():
    # download entire data from yfinace
    data = yf.download(sym, start="2000-01-01")

    # have onl;y two columns Date and Adj Close
    data = data['Adj Close']

    # reset index
    data = data.reset_index()

    # rename the columns to NAV Date and Nav
    data.columns = ['NAV Date', 'NAV']


    # save data to excel file to Data foler
    data.to_excel('Data/' + etf_name + '.xlsx', index=False)