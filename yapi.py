import datetime as dt
import pandas as pd
import pandas_datareader.data as web


PRICER_INV = "INV"
PRICER_ARB = "ARB"
PRICER_HFT = "HFT"
DB_ROOT_DIRECTORY = "C:/db/"
DB_INV_HISTDATA_STK_BARS = DB_ROOT_DIRECTORY + "db_mgr/db_securities/inv/db_histdata/stock_bars/"

start = dt.datetime(2000, 1, 1)
end = dt.datetime.now()
symbol = "QQQ"
df = web.DataReader(symbol, 'yahoo', start, end)




df.to_csv(symbol + '.csv')
print(df.head(6))