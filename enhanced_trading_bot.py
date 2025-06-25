import logging
import os
from binance import Client # type: ignore
import sys
from dotenv import load_dotenv # type: ignore
import time
from config import API_KEY, API_SECRET, TESTNET, LOG_LEVEL, LOG_FORMAT, LOG_FILE

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT, filename=LOG_FILE)
logger = logging.getLogger('bot_logger')

load_dotenv()

def sync_time(client):
    server_time = client.futures_time()['serverTime']
    local_time = int(time.time() * 1000)
    offset = server_time - local_time
    client.timestamp_offset = offset

class EnhancedTradingBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        sync_time(self.client)

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
                logger.error("Invalid order type")
                print("Invalid order type.")
                return None
            
            logger.info(f"Order placed: {order}")
            print("Order placed successfully:", order)
            return order
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            print(f"Order failed: {e}")
            return None

    def menu(self):
        print("\n=== Binance Futures Testnet Trading Bot ===")
        print("1. Place a new order")
        print("2. Exit")
        choice = input("Select an option (1-2): ").strip()
        return choice

    def get_order_details(self):
        print("\n--- Place a New Order ---")
        symbol = input("Trading pair (e.g., BTCUSDT): ").strip().upper()
        side = input("Order side (BUY/SELL): ").strip().upper()
        print("Order types: MARKET, LIMIT, STOP_MARKET, STOP_LIMIT, OCO")
        order_type = input("Order type: ").strip().upper()
        quantity = float(input("Quantity: "))
        price = None
        stop_price = None

        if order_type in ['LIMIT', 'STOP_LIMIT', 'OCO']:
            price = float(input("Limit price: "))
        if order_type in ['STOP_MARKET', 'STOP_LIMIT', 'OCO']:
            stop_price = float(input("Stop price: "))

        return symbol, side, order_type, quantity, price, stop_price

    def run(self):
        while True:
            choice = self.menu()
            if choice == '1':
                try:
                    symbol, side, order_type, quantity, price, stop_price = self.get_order_details()
                    self.place_order(symbol, side, order_type, quantity, price, stop_price)
                except Exception as e:
                    print(f"Error: {e}")
            elif choice == '2':
                print("Exiting bot. Goodbye!")
                break
            else:
                print("Invalid option. Please select 1 or 2.")

if __name__ == "__main__":
    # API keys are now imported from config.py
    if not API_KEY or not API_SECRET:
        logger.error("API key and secret must be set in config.py or environment variables.")
        sys.exit(1)
    
    print("API_KEY:", API_KEY)
    print("API_SECRET:", API_SECRET)
    
    bot = EnhancedTradingBot(API_KEY, API_SECRET, testnet=TESTNET)
    bot.run() 