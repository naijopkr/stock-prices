import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pandas_datareader import data, wb
from datetime import datetime
import eda
import plots

# SETUP
start = datetime(2006, 1, 1)
end = datetime(2016, 1, 2)
source = 'yahoo'
tickers = [
    'BAC',
    'C',
    'GS',
    'JPM',
    'MS',
    'WFC'
]

def fetch_data(ticker):
    return data.DataReader(ticker, source, start, end)

def get_head(ds):
    print(ds.head())
    print()


# Fetch data and define main dataset
stock_data = dict()
for ticker in tickers:
    stock_data[ticker] = fetch_data(ticker)
    get_head(stock_data[ticker])

bank_stocks = pd.concat(stock_data, axis=1)
bank_stocks.columns.names = ['Bank Ticker', 'Stock Info']


## EXPLORATORY DATA ANALYSIS (EDA) ##

# Subsets
stock_returns = eda.stock_returns(bank_stocks, tickers)

returns_2015 = eda.slice_dated_index(
    stock_returns,
    datetime(2014, 12, 31),
    datetime(2016, 1, 1)
)

returns_C_2008 = eda.slice_dated_index(
    stock_returns['C Return'],
    datetime(2007, 12, 31),
    datetime(2009, 1, 1)
)

stock_close = eda.subset(bank_stocks)
stock_close_reset = stock_close.reset_index()
stock_close_max = stock_close.max()

stock_close_bac = eda.slice_dated_index(
    stock_close['BAC'],
    datetime(2007, 12, 31),
    datetime(2009, 1, 1)
).reset_index()

close_price_corr = stock_close.corr()

bac_2015 = eda.slice_dated_index(
    stock_data['BAC'],
    datetime(2015, 1, 1),
    datetime(2016, 1, 1)
)
"""
# Print subsets heads
get_head(bank_stocks)
get_head(stock_returns)
get_head(returns_2015)
get_head(returns_C_2008)
get_head(stock_close)
get_head(stock_close_reset)
get_head(stock_close_max)
get_head(stock_close_bac)


# Max, min and std
eda.print_max(stock_returns)
eda.print_min(stock_returns)
eda.print_std(stock_returns)
eda.print_std(returns_2015)


## VISUALISATION ##

# Pairplot of stock returns
plots.pairplot(stock_returns, 'stock_returns')


# Distplot of MS Return in 2015
plots.distplot(returns_2015['MS Return'], bins=100, name='return_2015')


# Distplot of C Return in 2008
plots.distplot(returns_C_2008, bins=100, name='returns_C_2008.png')


# Lineplot for stock values
plots.multi_lineplot(stock_close_reset, tickers=tickers)


# Moving Averages
plots.moving_average(stock_close_bac, key='BAC')


# Heatmap and Clustermap with Close Price correlation
plots.heatmap(close_price_corr)
plots.clustermap(close_price_corr)
"""
# Create a candlestick plot for Bank of America
plots.candlestick(bac_2015, 'bac_2015')
