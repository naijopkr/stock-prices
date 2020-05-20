import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pandas_datareader import data, wb
from datetime import datetime

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

def fetch_data(symbol):
    return data.DataReader(symbol, source, start, end)

def get_head(ds):
    print(ds.head())
    print()

stock_data = dict()
for ticker in tickers:
    stock_data[ticker] = fetch_data(ticker)

for stock_ds in stock_data:
    get_head(stock_data[stock_ds])

bank_stocks = pd.concat(stock_data, axis=1)
bank_stocks.columns.names = ['Bank Ticker', 'Stock Info']
get_head(bank_stocks)
