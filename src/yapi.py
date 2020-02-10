import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import xlrd
import xlwt
from src import db_constants


def requestAllTickersBarDataAndSaveToDB(pricerType, startDate, endDate, barSize):
    allTickers = getAllTickers(pricerType)
    for ticker in allTickers:
        requestSingleTickerBarDataAndSaveToDB(ticker, startDate, endDate, barSize)


def getAllTickers(pricerType):
    if db_constants.PRICER_INV == pricerType:
        return pd.read_excel(db_constants.TABLE_INV_WATCHLIST, sheet_name='watch_list')[db_constants.WATCHLIST_HEADER[0]].tolist()
    elif db_constants.PRICER_ARB == pricerType:
        return pd.read_excel(db_constants.TABLE_ARB_WATCHLIST, sheet_name='watch_list')[db_constants.WATCHLIST_HEADER[0]].tolist()
    elif db_constants.PRICER_HFT == pricerType:
        return pd.read_excel(db_constants.TABLE_HFT_WATCHLIST, sheet_name='watch_list')[db_constants.WATCHLIST_HEADER[0]].tolist()

def requestSingleTickerBarDataAndSaveToDB(ticker, startDate, endDate, barSize):
    df = web.DataReader(ticker, 'yahoo', startDate, endDate)

    df.to_excel(db_constants.DB_INV_HISTDATA_STK_BARS + barSize + "_bar_prices/" + ticker + '.xls')
    print(df.head(6))


start = dt.datetime(2000, 1, 1)
end = dt.datetime.now()
barSize = 'd'

requestAllTickersBarDataAndSaveToDB(db_constants.PRICER_INV, start, end, barSize)
requestAllTickersBarDataAndSaveToDB(db_constants.PRICER_ARB, start, end, barSize)
requestAllTickersBarDataAndSaveToDB(db_constants.PRICER_HFT, start, end, barSize)