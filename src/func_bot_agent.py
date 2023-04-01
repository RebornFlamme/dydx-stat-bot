from func_private import place_market_order, check_order_status
from datetime import datetime, timedelta
import time 
from pprint import pprint 

# Class: Agent for managing opening and checking trades

class BotAgent:

    def __init__(
        self,
        client,
        market_1,
        market_2, 
        base_side, 
        base_size,
        base_price,
        quote_side,
        quote_size,
        quote_price,
        accept_failsafe_base_price,
        z_score,
        half_life,
        hedge_ratio
    ):
        # Initialize class variables
        self.client = client
        self.market_1 = market_1
        self.market_2 = market_2 
        self.base_side = base_side
        self.base_size = base_size
        self.base_price = base_price
        self.quote_side = quote_side 
        self.quote_size = quote_size
        self.quote_price = quote_price 
        self.accept_failsafe_base_price = accept_failsafe_base_price
        self.z_score = z_score 
        self.half_life = half_life
        self.hedge_ratio = hedge_ratio

        # Initialize output variables
        self.order_dict = {
            "market_1": market_1,
            "market_2": market_2,
            "hedge_ratio": hedge_ratio,
            "z_score": z_score,
            "half_life": half_life,
            "order_id_m1": "",
            "order_m1_size": base_size,
            "order_m1_side": base_side,
            "order_time_m1": "",
            "order_id_m2": "",
            "order_m2_size": quote_size,
            "order_m2_side": quote_side,
            "order_time_m2": "",
            "pair_status": "",
            "comments": ""

        }


    # Check order status by id 
    def check_order_status_by_id(self, order_id):

        # Allow time to process
        time.sleep(2)

        # Check order status
        order_status = check_order_status(self.client, order_id)

        # Guard: If order cancelled move onto next Pair
        if order_status == "CANCELED":
            print(f"{self.market_1} vs {self.market_2} - Order cancelled...")
            self.order_dict["pair_status"] = "FAILED"
            return "failed"

        # Guard: If order not filled wait until order expiration
        if order_status != "FAILED":
            time.sleep(15)
            order_status = check_order_status(self.client, order_id)

            # Guard: If order cancelled move onto next Pair
            if order_status == "CANCELED":
                print(f"{self.market_1} vs {self.market_2} - Order cancelled...")
                self.order_dict["pair_status"] = "FAILED"
                return "failed"

            # Guard: If not filled, cancel order
            if order_status != "FILLED":
                self.client.private.cancel_order(order_id=order_id)
                self.order_dict["pair_status"] = "ERROR"
                print(f"{self.market_1} vs {self.market_2} - Order error...")
                return "error"

        # Return live
        return "live"


    # Open trades
    def open_trades(self):
        
        # Print status
        print("-------------------------------------")
        print(f"{self.market_1}: Placing first order...")
        print(f"Side: {self.base_side}, Size: {self.base_size}, Price: {self.base_price}")
        print("-------------------------------------")

        # Place base order
        try:
            base_order = place_market_order(
                self.client,
                market=self.market_1,
                side=self.base_side,
                size=self.base_size,
                price=self.base_price
                reduce_only=False
            )




        except Exception as e:
            pass


    


    









        
