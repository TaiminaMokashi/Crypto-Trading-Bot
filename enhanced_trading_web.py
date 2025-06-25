from flask import Flask, render_template_string, request
from enhanced_trading_bot import EnhancedTradingBot
from config import API_KEY, API_SECRET, TESTNET, FLASK_HOST, FLASK_PORT, FLASK_DEBUG
import logging

app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Remove all handlers associated with the root logger object (to avoid duplicates)
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

file_handler = logging.FileHandler('web_bot.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info('Web logger test: Flask app started')

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Trading Bot Interface</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Mono:wght@700&display=swap" rel="stylesheet">
    <style>
        body { background: #181a1b; color: #fff; font-family: 'Fira Mono', monospace; }
        .container {
            background: #232526;
            max-width: 600px;
            margin: 60px auto;
            padding: 32px 32px 24px 32px;
            border-radius: 12px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.4);
        }
        h1 { font-size: 2rem; margin-bottom: 24px; font-weight: bold; }
        label { display: block; margin-top: 18px; margin-bottom: 6px; font-size: 1.1rem; }
        input, select {
            width: 100%;
            padding: 12px;
            background: #181a1b;
            border: 1px solid #333;
            border-radius: 6px;
            color: #fff;
            font-size: 1rem;
            margin-bottom: 8px;
        }
        button {
            background: #22c55e;
            color: #fff;
            border: none;
            padding: 12px 32px;
            border-radius: 6px;
            font-size: 1.1rem;
            font-weight: bold;
            margin-top: 12px;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background: #16a34a; }
        .result, .error {
            margin-top: 24px;
            padding: 16px;
            border-radius: 6px;
            font-size: 1rem;
        }
        .result { background: #1e293b; color: #22c55e; }
        .error { background: #1e293b; color: #ef4444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Trading Bot Interface</h1>
        <form method="post">
            <label>Trading Pair (e.g., BTCUSDT):</label>
            <input name="symbol" required>
            <label>Order Side (BUY/SELL):</label>
            <input name="side" required>
            <label>Order Type (MARKET/LIMIT/STOP_MARKET/STOP_LIMIT/OCO):</label>
            <select name="order_type" id="order_type" required onchange="updateFields()">
                <option value="MARKET">MARKET</option>
                <option value="LIMIT">LIMIT</option>
                <option value="STOP_MARKET">STOP_MARKET</option>
                <option value="STOP_LIMIT">STOP_LIMIT</option>
                <option value="OCO">OCO</option>
            </select>
            <label>Quantity:</label>
            <input name="quantity" type="number" step="0.0001" min="0.0001" required>
            <div id="price_field" style="display:none;">
                <label>Price:</label>
                <input name="price" type="number" step="0.0001" min="0">
            </div>
            <div id="stop_price_field" style="display:none;">
                <label>Stop Price:</label>
                <input name="stop_price" type="number" step="0.0001" min="0">
            </div>
            <button type="submit">Place Order</button>
        </form>
        <script>
            function updateFields() {
                var orderType = document.getElementById('order_type').value;
                document.getElementById('price_field').style.display = (orderType === 'LIMIT' || orderType === 'STOP_LIMIT' || orderType === 'OCO') ? '' : 'none';
                document.getElementById('stop_price_field').style.display = (orderType === 'STOP_MARKET' || orderType === 'STOP_LIMIT' || orderType === 'OCO') ? '' : 'none';
            }
            window.onload = updateFields;
        </script>
        {% if result %}
            <div class="result" style="text-align:center;">
                <img src="https://img.icons8.com/color/96/000000/ok--v1.png" alt="Success" style="width:64px;height:64px;"/><br>
                <b>Order placed successfully!</b>
            </div>
        {% endif %}
        {% if error %}
            <div class="error"><b>Error:</b> {{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        symbol = request.form['symbol'].strip().upper()
        side = request.form['side'].strip().upper()
        order_type = request.form['order_type'].strip().upper()
        quantity = float(request.form['quantity'])
        price = request.form.get('price')
        stop_price = request.form.get('stop_price')
        price = float(price) if price else None
        stop_price = float(stop_price) if stop_price else None
        try:
            bot = EnhancedTradingBot(API_KEY, API_SECRET, testnet=TESTNET)
            order = bot.place_order(symbol, side, order_type, quantity, price, stop_price)
            if order:
                result = order
                logger.info(f"Order placed successfully: {order}")
            else:
                error = "Order could not be placed. Check logs for details."
                logger.error(f"Order failed for {symbol} {side} {order_type} {quantity} {price} {stop_price}")
        except Exception as e:
            error = str(e)
            logger.error(f"Exception occurred: {e}")
    return render_template_string(HTML, result=result, error=error)

if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False, use_reloader=False) 