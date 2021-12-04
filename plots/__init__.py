import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
import plotly.io as pio

from pandas import DataFrame
from math_utils import geometric_mean

ROOT = "."


def pairplot(data: DataFrame, name: str):
    plt.figure()
    sns.pairplot(data[1:])
    plt.tight_layout()
    plt.savefig(f"{ROOT}/output/{name}.png")


def distplot(data: DataFrame, bins=30, name="output"):
    plt.figure()
    sns.distplot(data, bins=bins)
    plt.savefig(f"{ROOT}/output/{name}.png")


def multi_lineplot(
    data: DataFrame, x="Date", ylabel="Price (USD)", name="stock_close", tickers=[]
):
    plt.figure(figsize=(12, 4))
    for ticker in tickers:
        sns.lineplot(data=data, x=x, y=ticker, label=ticker)

    plt.ylabel(ylabel)
    plt.grid(b=True)
    plt.savefig(f"{ROOT}/output/{name}.png")


def moving_average(data: DataFrame, key: str, regular=20, geo=5, name="moving_average"):
    data[f"{regular}Day"] = data[key].rolling(window=regular).mean()
    data[f"{geo}Day"] = data[key].rolling(window=geo).apply(geometric_mean, raw=True)

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x=data.index, y="BAC", label="BAC")
    sns.lineplot(data=data, x=data.index, y=f"{regular}Day", label=f"{regular} day avg")
    sns.lineplot(data=data, x=data.index, y=f"{geo}Day", label=f"{geo} day avg")
    plt.savefig(f"{ROOT}/output/{name}.png")


def heatmap(data: DataFrame, name="heatmap"):
    plt.figure()
    sns.heatmap(data, cmap="coolwarm", annot=True)
    plt.savefig(f"{ROOT}/output/{name}.png")


def clustermap(data: DataFrame, name="clustermap"):
    plt.figure()
    sns.clustermap(data, cmap="coolwarm", annot=True)
    plt.savefig(f"{ROOT}/output/{name}.png")


def candlestick(data: DataFrame, name="candlestick"):
    candlestick_data = go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="BAC",
    )

    ma5 = data["Close"].rolling(window=5).mean()
    ma20 = data["Close"].rolling(window=20).mean()

    ma5_data = go.Scatter(
        x=data.index, y=ma5, name="MA5", line=dict(color="orange", width=1)
    )
    ma20_data = go.Scatter(
        x=data.index, y=ma20, name="MA20", line=dict(color="green", width=1)
    )

    candlestick_plot = go.Figure(data=[candlestick_data, ma5_data, ma20_data])

    pio.write_html(candlestick_plot, f"{ROOT}/output/{name}.html", auto_open=True)


def candlestick_boll(data: DataFrame, name="dataframe_boll"):
    candlestick_data = go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="BAC",
    )

    ma20 = data["Close"].rolling(window=20).mean()
    k_sigma = data["Close"].rolling(window=20).std() * 2
    upper = ma20 + k_sigma
    lower = ma20 - k_sigma

    ma20_data = go.Scatter(
        x=data.index, y=ma20, name="MA20", line=dict(color="blue", width=1)
    )
    upper_band = go.Scatter(
        x=data.index, y=upper, name="upperBB", line=dict(color="red", width=1)
    )
    lower_band = go.Scatter(
        x=data.index, y=lower, name="lowerBB", line=dict(color="green", width=1)
    )

    candlestick_plot = go.Figure(
        data=[candlestick_data, upper_band, ma20_data, lower_band]
    )

    pio.write_html(candlestick_plot, f"{ROOT}/output/{name}.html", auto_open=True)
