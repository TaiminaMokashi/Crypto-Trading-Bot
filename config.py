# Shared configuration for all trading bots
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_KEY = '4bf218db27887f1ad27998654ade8ba4ef7e6a95f2370851b6e6e480bbad3ba6'
API_SECRET = 'd80dcfdbd31f6ee5d0dae7ac982a0e681336ed50242b322969fab82dd26f5fe0'

# Trading Configuration
DEFAULT_SYMBOL = 'BTCUSDT'
DEFAULT_QUANTITY = 0.002
TESTNET = True

# Flask Configuration
FLASK_HOST = '127.0.0.1'
FLASK_PORT = 5000
FLASK_DEBUG = True

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = 'bot.log' 