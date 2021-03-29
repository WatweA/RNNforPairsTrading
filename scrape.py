#!/usr/bin/python

import time
from datetime import datetime
import numpy as np
import pandas as pd
import pandas_datareader as pdr


tickers = dict()
with open("tickers.txt") as f:
    # reader the header line
    headers = f.readline().strip().lower().split(",")
    tickers = {header: [] for header in headers}
    
    # simulate a do-while loop by reading the next line and checking that it is non-empty
    while True:
        line = f.readline().strip()
        if line == '':
            break

        # create a list divided by "," and append the entry into its header's list of values
        line = line.split(",")
        for (index, header) in enumerate(headers):
            tickers[header].append(line[index])


for ticker in tickers["symbol"]:
    try:
        df = pdr.get_data_yahoo(symbols=ticker, start=datetime(1999, 1, 4), end=datetime(2021, 3, 1))
        if str(df.index[0]) == '1999-01-04 00:00:00' and str(df.index[-1]) == '2021-03-01 00:00:00':
            df["Simple Return"] = (df["Adj Close"] - df["Adj Close"].shift(1)) / df["Adj Close"]
            df["Log Return"] = np.log(df["Adj Close"]) - np.log(df["Adj Close"].shift(1))
            df.to_pickle("data/raw/" + ticker + ".zip")
            print(f"saved {ticker}")
        else:
            print(f"skipping {ticker}: 1999-01-04 data and/or 2021-03-01 DNE")
    except Exception:
        print(f"API ERROR {ticker}")
    
    time.sleep(1)  # to avoid spamming the Yahoo! API

