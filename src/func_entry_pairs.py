from pandas.core import base, series
from constants import ZSCORE_TRESH, USD_PER_TRADE, USD_MIN_COLLATERAL
from func_utils import format_number
from func_public import get_candles_recent
from func_cointegration import calculate_zscore
from func_private import is_open_positions
from func_bot_agent import BotAgent

import pandas as pd 
import json
from pprint import pprint 

# Open positions 
def open_positions(client):
    
    """
        Manage finding triggers for trade entry 
        Store trades for managing later on exit function  
    """

    # Load cointegrated pairs
    df = pd.read_csv("cointegrated_pairs.csv")

    # Get markets for referencing min order size and tick size
    markets = client.public.get_markets().data

    # Initialize
    bot_agents = []

    # Find ZScore triggers
    for index, row in df.iterrows():

        # Extract variables
        base_market = row["base_market"]
        quote_market = row["quote_market"]
        hedge_ratio = row["hedge_ratio"]
        half_life = row["half_life"]

        # get prices
        series_1 = get_candles_recent(client, base_market)
        series_2 = get_candles_recent(client, quote_market)

        # Get ZScore 
        if len(series_1) > 0 and len(series_1) == len(series_2):
            spread = series_1 - (hedge_ratio * series_2)
            z_score = calculate_zscore(spread).values.tolist()[-1]

            # Establish if potential trade 
            if abs(z_score) >= ZSCORE_TRESH:

                # Ensure that the trade was not opened before
                is_base_open = is_open_positions(client, base_market)
                is_quote_open = is_open_positions(client, quote_market)

                # Place trade
                if not is_base_open and not is_quote_open:

                    base_side = "BUY" if z_score < 0 else "SELL"
                    quote_side = "SELL" if z_score < 0 else "BUY"

                    # Get acceptable price in string format with correct number of decimals 
                    base_price = series_1[-1]
                    quote_price = series_2[-1]
                    accept_base_price = float(base_price) * 1.01 if z_score < 0 else float(base_price) * 0.99
                    accept_quote_price = float(quote_price) * 1.01 if z_score > 0 else float(quote_price) * 0.99



                


