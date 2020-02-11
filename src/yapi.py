import sys
print(sys.path)
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import xlrd
import xlwt
from src import db_constants
from src.security_util import SecurityUtil


def getAllTickers(pricerType):
    if db_constants.PRICER_INV == pricerType:
        return pd.read_excel(db_constants.TABLE_INV_WATCHLIST, sheet_name='watch_list')[db_constants.WATCHLIST_HEADER[0]].tolist()
    elif db_constants.PRICER_ARB == pricerType:
        return pd.read_excel(db_constants.TABLE_ARB_WATCHLIST, sheet_name='watch_list')[db_constants.WATCHLIST_HEADER[0]].tolist()
    elif db_constants.PRICER_HFT == pricerType:
        return pd.read_excel(db_constants.TABLE_HFT_WATCHLIST, sheet_name='watch_list')[db_constants.WATCHLIST_HEADER[0]].tolist()

def requestSingleTickerBarDataAndSaveToDB(pricerType, ticker, startDate, endDate, barSize):
    # core pandas datareader API
    df = web.DataReader(ticker, 'yahoo', startDate, endDate)
    # df = pd.read_excel(db_constants.DB_INV_HISTDATA_STK_BARS + barSize + "_bar_prices/" + ticker + '.xls', sheet_name=0, index_col=0);
    df.reset_index(inplace=True)
    # rename columns
    df.columns = ['open_date', 'high_price', 'low_price', 'open_price', 'close_price', 'volume', 'adjusted_close_price']
    # reorder columns
    df = df[['open_date', 'open_price', 'high_price', 'low_price', 'close_price', 'adjusted_close_price', 'volume']]
    # change open_date column type from datetime64 to str
    df['open_date'] = df['open_date'].astype('str')

    if db_constants.PRICER_INV == pricerType:
        df.to_excel(db_constants.DB_INV_HISTDATA_STK_BARS + barSize + "_bar_prices/" + ticker + '.xls', sheet_name=ticker, index=False)
    elif db_constants.PRICER_ARB == pricerType:
        df.to_excel(db_constants.DB_ARB_HISTDATA_STK_BARS + barSize + "_bar_prices/" + ticker + '.xls', sheet_name=ticker, index=False)
    elif db_constants.PRICER_HFT == pricerType:
        df.to_excel(db_constants.DB_HFT_HISTDATA_STK_BARS + barSize + "_bar_prices/" + ticker + '.xls', sheet_name=ticker, index=False)

def requestAllTickersBarDataAndSaveToDB(pricerType, startDate, endDate, barSize):
    allTickers = getAllTickers(pricerType)
    for ticker in allTickers:
        ticker = SecurityUtil.chopExchangeCodeSuffix(SecurityUtil.chopExchangeCodePrefix(ticker))
        requestSingleTickerBarDataAndSaveToDB(pricerType, ticker, startDate, endDate, barSize)
        print("{}: {} has been successfuly saved!".format(pricerType, ticker))

def main():
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime.now()
    barSize = 'd'

    requestAllTickersBarDataAndSaveToDB(db_constants.PRICER_INV, start, end, barSize)
    requestAllTickersBarDataAndSaveToDB(db_constants.PRICER_ARB, start, end, barSize)
    requestAllTickersBarDataAndSaveToDB(db_constants.PRICER_HFT, start, end, barSize)

if __name__ == '__main__':
    main()
