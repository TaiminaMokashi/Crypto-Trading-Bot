# Binance Trading Bot Project

## Overview
This project is a Binance Futures trading bot with both a web interface (Flask) and a command-line interface (CLI). It allows you to place various types of orders (MARKET, LIMIT, STOP_MARKET, STOP_LIMIT, OCO) on the Binance Futures Testnet. All order activity is logged for auditing and debugging.

## Features
- Place orders via a modern web interface or CLI
- Supports MARKET, LIMIT, STOP_MARKET, STOP_LIMIT, and OCO order types
- Logging of all order activity and errors
- Easy configuration via `config.py`

## Setup Instructions

1. **Clone or Download the Project**
   - Download the ZIP or clone the repository to your local machine.

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys and Settings**
   - Edit `config.py` and set your Binance API key and secret (use testnet keys for safety).
   - Adjust other settings (host, port, logging) as needed.

## Usage

### Web Interface (Recommended)
1. Run the web app:
   ```bash
   python enhanced_trading_web.py
   ```
2. Open your browser and go to [http://127.0.0.1:5000]
3. Fill out the form to place an order. A success image will appear if the order is placed successfully.
4. All order activity is logged in `web_bot.log`.

### Command-Line Interface (CLI)
1. Run the CLI bot:
   ```bash
   python enhanced_trading_bot.py
   ```
2. Follow the prompts to place orders from the terminal.
3. All order activity is logged in `bot.log`.

## Logging
- **Web interface logs:** `web_bot.log`
- **CLI bot logs:** `bot.log`
- Logs include all order details, errors, and server activity for auditing and debugging.


## Notes
- This project is for educational and assignment purposes. **Do not use real funds or mainnet API keys.**
- For any issues, please check the log files for detailed error messages.
