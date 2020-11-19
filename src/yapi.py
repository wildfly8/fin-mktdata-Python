from src import db_constants
from src.security_util import SecurityUtil
import sys
print("Python_Version: {}, Python_Path: {}".format(sys.version, sys.path))
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import xlrd
import xlwt
# import requests

def getAllTickers(pricerType):
    if db_constants.PRICER_INV == pricerType:
        return pd.read_excel(db_constants.TABLE_INV_WATCHLIST, sheet_name='watch_list')[
            db_constants.WATCHLIST_HEADER[0]].tolist()
    elif db_constants.PRICER_ARB == pricerType:
        return pd.read_excel(db_constants.TABLE_ARB_WATCHLIST, sheet_name='watch_list')[
            db_constants.WATCHLIST_HEADER[0]].tolist()
    elif db_constants.PRICER_HFT == pricerType:
        return pd.read_excel(db_constants.TABLE_HFT_WATCHLIST, sheet_name='watch_list')[
            db_constants.WATCHLIST_HEADER[0]].tolist()


def requestSingleTickerBarDataAndSaveToDB(pricerType, ticker, startDate, endDate, barSize):
    # prepare valid ticker for Yahoo API
    ticker = SecurityUtil.chopExchangeCodePrefix(ticker)
    yahooTicker = SecurityUtil.getYahooAPITicker(ticker)
    ticker = SecurityUtil.chopExchangeCodeSuffix(ticker)
    # core pandas datareader API
    df = web.DataReader(yahooTicker, 'yahoo', startDate, endDate)
    # df = pd.read_excel(db_constants.DB_INV_HISTDATA_STK_BARS + barSize + "_bar_prices/" + ticker + '.xls', sheet_name=0, index_col=0);
    df.reset_index(inplace=True)
    # rename columns
    df.columns = ['open_date', 'high_price', 'low_price', 'open_price', 'close_price', 'volume', 'adjusted_close_price']
    # reorder columns
    df = df[['open_date', 'open_price', 'high_price', 'low_price', 'close_price', 'adjusted_close_price', 'volume']]
    # change open_date column type from datetime64 to str
    df['open_date'] = df['open_date'].astype('str')

    if db_constants.PRICER_INV == pricerType:
        df.to_excel(db_constants.DB_INV_HISTDATA_STK_BARS + barSize + "_bar_prices/" + ticker + '.xls',
                    sheet_name=ticker, index=False)
    elif db_constants.PRICER_ARB == pricerType:
        df.to_excel(db_constants.DB_ARB_HISTDATA_STK_BARS + barSize + "_bar_prices/" + ticker + '.xls',
                    sheet_name=ticker, index=False)
    elif db_constants.PRICER_HFT == pricerType:
        df.to_excel(db_constants.DB_HFT_HISTDATA_STK_BARS + barSize + "_bar_prices/" + ticker + '.xls',
                    sheet_name=ticker, index=False)


def requestAllTickersBarDataAndSaveToDB(pricer_type, start_date, end_date, bar_size):
    all_tickers = getAllTickers(pricer_type)
    for ticker in all_tickers:
        try:
            requestSingleTickerBarDataAndSaveToDB(pricer_type, ticker, start_date, end_date, bar_size)
            print("{}: {} daily bar is successfuly saved.".format(pricer_type, ticker))
        except Exception as e:
            print("{}: {} daily bar fails to be saved! Reason: {}".format(pricer_type, ticker, e))


def main():
    end = dt.datetime.now()
    start = dt.datetime(2000, 1, 1)
    bar_size = 'd'
    requestAllTickersBarDataAndSaveToDB(db_constants.PRICER_INV, start, end, bar_size)
    requestAllTickersBarDataAndSaveToDB(db_constants.PRICER_ARB, start, end, bar_size)
    requestAllTickersBarDataAndSaveToDB(db_constants.PRICER_HFT, start, end, bar_size)
    print("Elapsed Time = {0} sec".format(dt.datetime.now() - end))


if __name__ == '__main__':
    main()
