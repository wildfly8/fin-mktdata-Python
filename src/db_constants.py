DB_ROOT_DIRECTORY = "C:/db/"

PRICER_INV = "INV"
PRICER_ARB = "ARB"
PRICER_HFT = "HFT"

TABLE_INV_WATCHLIST = DB_ROOT_DIRECTORY + "db_mgr/db_securities/inv/db_watchlist/watch_list.xls"
TABLE_ARB_WATCHLIST = DB_ROOT_DIRECTORY + "db_mgr/db_securities/arb/db_watchlist/watch_list.xls"
TABLE_HFT_WATCHLIST = DB_ROOT_DIRECTORY + "db_mgr/db_securities/hft/db_watchlist/watch_list.xls"

DB_INV_HISTDATA_STK_BARS = DB_ROOT_DIRECTORY + "db_mgr/db_securities/inv/db_histdata/stock_bars/"
DB_ARB_HISTDATA_STK_BARS = DB_ROOT_DIRECTORY + "db_mgr/db_securities/arb/db_histdata/stock_bars/"
DB_HFT_HISTDATA_STK_BARS = DB_ROOT_DIRECTORY + "db_mgr/db_securities/hft/db_histdata/stock_bars/"

WATCHLIST_HEADER = ["symbol", "exch.", "sector", "market_cap", "out_shares", "float%", "employees", "avg_vol", "short_ratio", "insider_own", "inst_own", \
                    "next_earnings_date", "next_ex_date", "div_yield", "trailing_PE (ttm)", "forward_PE (ttm)", "P/S (ttm)", "P/B (mrq)", "profit_margin (ttm)", \
                    "operating_margin (ttm)", "ROA (ttm)", "ROE (ttm)", "revenue (ttm)", "qtrly_revenue_growth (yoy)", "EBITDA (ttm)", "NIAC (ttm)", "qtrly_earnings_growth", \
                    "total_cash", "total_debt", "operating_cashflow (ttm)", "levered_free_cashflow (ttm)"]