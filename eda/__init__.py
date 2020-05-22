from pandas import DataFrame
from datetime import datetime

def subset(
    data: DataFrame,
    key='Close',
    axis=1,
    level='Stock Info',
    reset_index = False
):
    sub = data.xs(key=key, level=level, axis=axis)

    if reset_index:
        return sub.reset_index()

    return sub


def max_close(data: DataFrame):
    return data.max()

def stock_returns(data: DataFrame, tickers = []):
    returns_ds = DataFrame()
    for ticker in tickers:
        pct_return = data[ticker]['Close'].pct_change()
        returns_ds[f'{ticker} Return'] = pct_return

    return returns_ds


def print_max(data: DataFrame):
    print(f'Max value: {data.idxmax()}')
    print()


def print_min(data: DataFrame):
    print(f'Min value: {data.idxmin()}')
    print()


def print_std(data: DataFrame):
    print(f'Standard deviation: {data.std()}')
    print()


def slice_dated_index(data: DataFrame, start: datetime, end: datetime):
    sliced_data = data.loc[
        (data.index > start) &
        (data.index < end)
    ]

    return sliced_data
