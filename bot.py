import logging
import os
from binance import Client # type: ignore
import sys
from config import API_KEY, API_SECRET, TESTNET, LOG_LEVEL, LOG_FORMAT, LOG_FILE

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT, filename=LOG_FILE)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            if order_type == 'MARKET':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            elif order_type == 'LIMIT':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity,
                    price=price,
                    timeInForce='GTC'
                )
            elif order_type == 'STOP_MARKET':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='STOP_MARKET',
                    quantity=quantity,
                    stopPrice=stop_price
                )
            elif order_type == 'STOP_LIMIT':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='STOP_LIMIT',
                    quantity=quantity,
                    price=price,
                    stopPrice=stop_price,
                    timeInForce='GTC'
                )
            elif order_type == 'OCO':
                order = self.client.futures_create_oco_order(
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    price=price,
                    stopPrice=stop_price,
                    stopLimitPrice=stop_price,  # You can adjust this as needed
                    stopLimitTimeInForce='GTC'
                )
            else:
                logging.error("Invalid order type")
                return None
            
            logging.info(f"Order placed: {order}")
            return order
        except Exception as e:
            logging.error(f"Error placing order: {e}")
            return None

    def get_user_input(self):
        try:
            symbol = input("Enter trading pair (e.g., BTCUSDT): ")
            side = input("Enter order side (BUY/SELL): ").upper()
            order_type = input("Enter order type (MARKET/LIMIT/STOP_MARKET/STOP_LIMIT/OCO): ").upper()
            quantity = float(input("Enter quantity: "))
            price = None
            stop_price = None
            
            if order_type in ['LIMIT', 'STOP_LIMIT', 'OCO']:
                price = float(input("Enter limit price: "))
            if order_type in ['STOP_MARKET', 'STOP_LIMIT', 'OCO']:
                stop_price = float(input("Enter stop price: "))
            
            return symbol, side, order_type, quantity, price, stop_price
        except ValueError as e:
            logging.error(f"Invalid input: {e}")
            sys.exit(1)

    def run(self):
        symbol, side, order_type, quantity, price, stop_price = self.get_user_input()
        self.place_order(symbol, side, order_type, quantity, price, stop_price)

if __name__ == "__main__":
    # API keys are now imported from config.py
    if not API_KEY or not API_SECRET:
        logging.error("API key and secret must be set in config.py or environment variables.")
        sys.exit(1)
    
    bot = BasicBot(API_KEY, API_SECRET, testnet=TESTNET)
    bot.run()
