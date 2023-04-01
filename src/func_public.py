from constants import RESOLUTION
from func_utils import get_ISO_times
from pprint import pprint 

import pandas as pd 
import numpy as np 
import time 

ISO_TIMES = get_ISO_times()


# Get Candles Historical
def get_candles_historical(client, market):

    # Define output
    close_prices = []

    # Extract historical data for each timeframe
    for timeframe in ISO_TIMES.keys():

        tf_obj = ISO_TIMES[timeframe]
        from_iso = tf_obj["from_iso"]
        to_iso = tf_obj["to_iso"]

        time.sleep(0.2)

        candles = client.public.get_candles(
            market = market,
            resolution = RESOLUTION,
            from_iso = from_iso,
            to_iso = to_iso,
            limit=100
        )

        # Structure Data
        for candle in candles.data["candles"]:
            close_prices.append({"datetime": candle['startedAt'], market: candle["close"]})

    # Construct and return Dataframe
    close_prices.reverse()
    return close_prices


# Construct market prices
def construct_market_prices(client):
    
    # Declare variables 
    tradeable_markets = []
    markets = client.public.get_markets()

    # Find tradeables pairs 
    for market in markets.data["markets"].keys():
        market_info = markets.data["markets"][market]
        if market_info["status"] == "ONLINE" and market_info["type"] == "PERPETUAL":
            tradeable_markets.append(market)

    # Set initial Dataframe
    close_prices = get_candles_historical(client, tradeable_markets[0])
    df = pd.DataFrame(close_prices)
    df.set_index("datetime", inplace=True)


    # Append other prices 
    for market in tradeable_markets:
        close_prices_add = get_candles_historical(client, market)
        df_add = pd.DataFrame(close_prices_add)
        df_add.set_index("datetime", inplace=True)
        df = pd.merge(df, df_add, how="outer", on="datetime", copy=False)
        del df_add

    # Check NaN
    nans = df.columns[df.isna().any()].to_list()
    if len(nans) > 0:
        print("Dropping columns")
        print(nans)
        df.drop(columns=nans, inplace=True)

    print(df.tail())

    return df

