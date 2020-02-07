import datetime as dt
import pandas as pd
import pandas_datareader.data as web

start = dt.datetime(2000, 1, 1)
end = dt.datetime.now()
df = web.DataReader("SPY", 'yahoo', start, end)
df.to_csv('SPY.csv')
print(df.head(6))