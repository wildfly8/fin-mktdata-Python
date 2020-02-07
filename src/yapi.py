import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import xlrd
from src import db_constants

excel_watchlist_df = pd.read_excel(db_constants.TABLE_INV_WATCHLIST, sheet_name='watch_list')
print(excel_watchlist_df[db_constants.WATCHLIST_HEADER[0]].tolist())



start = dt.datetime(2000, 1, 1)
end = dt.datetime.now()
# symbol = "QQQ"
# df = web.DataReader(symbol, 'yahoo', start, end)
#
# df.to_csv(symbol + '.csv')
# print(df.head(6))