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


