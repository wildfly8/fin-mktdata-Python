from src import db_constants
from src.security_util import SecurityUtil
import sys

print("Python_Version: {}, Python_Path: {}".format(sys.version, sys.path))
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
from pyspark.sql import SparkSession
import xlrd
import xlwt
# import requests

def get_all_tickers(pricer_type):
    if db_constants.PRICER_INV == pricer_type:
        return pd.read_excel(db_constants.TABLE_INV_WATCHLIST, sheet_name='watch_list')[db_constants.WATCHLIST_HEADER[0]].tolist()
    elif db_constants.PRICER_ARB == pricer_type:
        return pd.read_excel(db_constants.TABLE_ARB_WATCHLIST, sheet_name='watch_list')[db_constants.WATCHLIST_HEADER[0]].tolist()
    elif db_constants.PRICER_HFT == pricer_type:
        return pd.read_excel(db_constants.TABLE_HFT_WATCHLIST, sheet_name='watch_list')[db_constants.WATCHLIST_HEADER[0]].tolist()


def request_single_ticker_bar_data_and_save_to_db(pricer_type, ticker, start_date, end_date, bar_size):
    # prepare valid ticker for Yahoo API
    ticker = SecurityUtil.chopExchangeCodePrefix(ticker)
    yahoo_ticker = SecurityUtil.getYahooAPITicker(ticker)
    ticker = SecurityUtil.chopExchangeCodeSuffix(ticker)
    # core pandas datareader API
    df = web.DataReader(yahoo_ticker, 'yahoo', start_date, end_date)
    df.reset_index(inplace=True)
    # rename columns
    df.columns = ['open_date', 'high_price', 'low_price', 'open_price', 'close_price', 'volume', 'adjusted_close_price']
    # reorder columns
    df = df[['open_date', 'open_price', 'high_price', 'low_price', 'close_price', 'adjusted_close_price', 'volume']]
    # change open_date column type from datetime64 to str
    df['open_date'] = df['open_date'].astype('str')

    if db_constants.PRICER_INV == pricer_type:
        df.to_excel(db_constants.DB_INV_HISTDATA_STK_BARS + bar_size + "_bar_prices/" + ticker + '.xls', sheet_name=ticker, index=False)
    elif db_constants.PRICER_ARB == pricer_type:
        df.to_excel(db_constants.DB_ARB_HISTDATA_STK_BARS + bar_size + "_bar_prices/" + ticker + '.xls', sheet_name=ticker, index=False)
    elif db_constants.PRICER_HFT == pricer_type:
        df.to_excel(db_constants.DB_HFT_HISTDATA_STK_BARS + bar_size + "_bar_prices/" + ticker + '.xls', sheet_name=ticker, index=False)


def request_all_tickers_bar_data_and_save_to_db(pricer_type, start_date, end_date, bar_size, spark):
    rdd_all_tickers = spark.sparkContext.parallelize(get_all_tickers(pricer_type))
    sum_success = spark.sparkContext.accumulator(0)
    sum_failure = spark.sparkContext.accumulator(0)
    rdd_all_tickers.foreach(lambda ticker: request_for_ticker(pricer_type, ticker, start_date, end_date, bar_size, sum_success, sum_failure))
    print("{}: {} # of daily bars successfully saved. {} # of daily bars failed to be saved!".format(pricer_type, sum_success.value, sum_failure.value))


def request_for_ticker(pricer_type, ticker, start_date, end_date, bar_size, sum_success, sum_failure):
    try:
        request_single_ticker_bar_data_and_save_to_db(pricer_type, ticker, start_date, end_date, bar_size)
        sum_success.add(1)
        print("{}: {} daily bar is successfuly saved.".format(pricer_type, ticker))
    except Exception as e:
        sum_failure.add(1)
        print("{}: {} daily bar fails to be saved! Reason: {}".format(pricer_type, ticker, e))


def main():
    end = dt.datetime.now()
    start = dt.datetime(2000, 1, 1)
    bar_size = 'd'
    # pyspark
    spark = SparkSession.builder \
        .appName('yapi-pyspark') \
        .master('local[*]') \
        .getOrCreate()
    request_all_tickers_bar_data_and_save_to_db(db_constants.PRICER_INV, start, end, bar_size, spark)
    request_all_tickers_bar_data_and_save_to_db(db_constants.PRICER_ARB, start, end, bar_size, spark)
    request_all_tickers_bar_data_and_save_to_db(db_constants.PRICER_HFT, start, end, bar_size, spark)
    print("Elapsed Time = {0}".format(dt.datetime.now() - end))
    spark.stop()


if __name__ == '__main__':
    main()
