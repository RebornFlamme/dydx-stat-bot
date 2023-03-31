from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
import datetime
from pprint import pprint

if __name__ == "__main__":

    # Connect to client 
    try:
        print("Connecting to client...")
        client = connect_dydx()
    except Exception as e:
        print(e)
        print("Error connecting to client:", e)
        exit(1)



# Abort all open positions 
if ABORT_ALL_POSITIONS:
    try:
        print("Closing all positions...")
        close_orders = abort_all_positions(client)
        pprint(close_orders)

    except Exception as e:
        print(e)
        print("Error closing all positions", e)
        exit(1)

# Find Cointegrated Pairs
if FIND_COINTEGRATED:
    try:
        print("Fetching market prices...")
        df_market_prices = construct_market_prices(client)

    except Exception as e:
        print(e)
        print("Error constructing market prices", e)
        exit(1)
