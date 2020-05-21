import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pandas_datareader import data, wb
from datetime import datetime

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

def fetch_data(symbol):
    return data.DataReader(symbol, source, start, end)

def get_head(ds):
    print(ds.head())
    print()

stock_data = dict()
for ticker in tickers:
    stock_data[ticker] = fetch_data(ticker)
    get_head(stock_data[ticker])

bank_stocks = pd.concat(stock_data, axis=1)
bank_stocks.columns.names = ['Bank Ticker', 'Stock Info']
get_head(bank_stocks)

# EDA
max_close = bank_stocks.xs(key='Close', axis=1, level='Stock Info').max()
get_head(max_close)

stock_returns = pd.DataFrame()
for tick in tickers:
    stock_returns[tick + ' Return'] = bank_stocks[tick]['Close'].pct_change()

get_head(stock_returns)

### Pair plot
# sns.pairplot(stock_returns[1:])
# plt.tight_layout()
# plt.savefig('output/stock_returns.png')

print(stock_returns.idxmin())
print()
print(stock_returns.idxmax())
print()

### Verify prices in date range that differs from solution
# c_returns = stock_returns['C Return']
# c_returns_date = c_returns[
#     (c_returns.index > datetime(2011, 5, 1)) &
#     (c_returns.index < datetime(2011, 5, 11))
# ]

# banks_close = bank_stocks['C']['Close']
# banks_close_date = banks_close[
#     (banks_close.index > datetime(2011, 5, 1)) &
#     (banks_close.index < datetime(2011, 5, 11))
# ]

# print(c_returns_date)
# print()
# print(banks_close_date)

print(stock_returns.std())
print()

returns_2015 = stock_returns.loc[
    (stock_returns.index > datetime(2014, 12, 31)) &
    (stock_returns.index < datetime(2016, 1, 1))
]
print(returns_2015.std())
print()

# Dist plot of MS Return in 2015
# sns.distplot(returns_2015['MS Return'], bins=100)
# plt.savefig('output/return_2015.png')

# Dist plot of C Return in 2008
returns_C_2008 = stock_returns['C Return'].loc[
    (stock_returns.index > datetime(2007, 12, 31)) &
    (stock_returns.index < datetime(2009, 1, 1))
]
get_head(returns_C_2008)

# sns.distplot(returns_C_2008, bins=100)
# plt.savefig('output/returns_C_2008.png')

# MORE VISUALIZATION
stock_close = bank_stocks.xs('Close', axis=1, level='Stock Info').reset_index()
get_head(stock_close)

# Lineplot for stock values
# fig = plt.figure(figsize=(15,5))
# for tick in tickers:
#     sns.lineplot(data=stock_close, x='Date', y=tick, label=tick)

# plt.set_cmap('viridis')
# plt.ylabel('Price (USD)')
# plt.grid(b=True)
# plt.savefig('output/stock_close.png')


# Moving Averages
plt.figure(figsize=(12,6))
stock_close_bac = stock_close[['Date', 'BAC']][
    (stock_close['Date'] > datetime(2007, 12, 31)) &
    (stock_close['Date'] < datetime(2009, 1, 1))
]
get_head(stock_close_bac)

def geometric_mean(values):
    product = 1
    for value in values:
        product *= value

    return product ** (1/len(values))

stock_close_bac['20Day'] = stock_close_bac['BAC'].rolling(window=20).mean()
stock_close_bac['5Day'] = stock_close_bac['BAC'].rolling(
    window=5
).apply(
    geometric_mean,
    raw=True
)
print(stock_close_bac.tail())
print()

# sns.lineplot(data=stock_close_bac, x='Date', y='BAC', label='BAC')
# sns.lineplot(data=stock_close_bac, x='Date', y='20Day', label='20 day avg')
# sns.lineplot(data=stock_close_bac, x='Date', y='5Day', label='5 day avg')
# plt.savefig('output/stock_close_bac.png')

# Heatmap with Close Price correlation
close_price = bank_stocks.xs('Close', axis=1, level='Stock Info')
get_head(close_price)

# sns.heatmap(close_price.corr(), cmap='coolwarm', annot=True)
# plt.savefig('output/correlation_heatmap.png')

# sns.clustermap(close_price.corr(), cmap='coolwarm', annot=True)
# plt.savefig('output/correlation_clustermap.png')
