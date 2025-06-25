from flask import Flask, render_template_string, request # type: ignore
from binance import Client # type: ignore
from config import API_KEY, API_SECRET, FLASK_HOST, FLASK_PORT, FLASK_DEBUG

# --- Your API keys here (or use environment variables) ---
# API keys are now imported from config.py

client = Client(API_KEY, API_SECRET, testnet=True)

app = Flask(__name__)      

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title> Binance Futures Testnet Trading Bot </title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 500px; margin: auto; }
        input, select { width: 100%; padding: 8px; margin: 8px 0; }
        button { padding: 10px 20px; }
        .success { color: green; }
        .error { color: red; }
        .order-details { background: #f4f4f4; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Binance Futures Testnet Trading Bot</h2>
        <form method="post">
            <label>Trading Pair:</label>
            <input name="symbol" value="BTCUSDT" required>
            <label>Side:</label>
            <select name="side">
                <option>BUY</option>
                <option>SELL</option>
            </select>
            <label>Order Type:</label>
            <select name="order_type" id="order_type" onchange="showHideFields()">
                <option>MARKET</option>
                <option>LIMIT</option>
                <option>STOP_MARKET</option>
                <option>STOP_LIMIT</option>
            </select>
            <label>Quantity:</label>
            <input name="quantity" type="number" step="0.001" min="0.001" value="0.002" required>
            <div id="limit_fields" style="display:none;">
                <label>Limit Price:</label>
                <input name="price" type="number" step="0.01" min="0">
            </div>
            <div id="stop_fields" style="display:none;">
                <label>Stop Price:</label>
                <input name="stop_price" type="number" step="0.01" min="0">
            </div>
            <button type="submit">Place Order</button>
        </form>
        {% if result %}
            <div class="order-details">
                <h4>Order Result:</h4>
                <pre>{{ result }}</pre>
            </div>
        {% endif %}
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
    </div>
    <script>
        function showHideFields() {
            var orderType = document.getElementById('order_type').value;
            document.getElementById('limit_fields').style.display = (orderType == 'LIMIT' || orderType == 'STOP_LIMIT') ? 'block' : 'none';
            document.getElementById('stop_fields').style.display = (orderType == 'STOP_MARKET' || orderType == 'STOP_LIMIT') ? 'block' : 'none';
        }
        window.onload = showHideFields;
    </script>
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

        try:
            if order_type == 'MARKET':
                order = client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            elif order_type == 'LIMIT':
                order = client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity,
                    price=price,
                    timeInForce='GTC'
                )
            elif order_type == 'STOP_MARKET':
                order = client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='STOP_MARKET',
                    quantity=quantity,
                    stopPrice=stop_price
                )
            elif order_type == 'STOP_LIMIT':
                order = client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='STOP_LIMIT',
                    quantity=quantity,
                    price=price,
                    stopPrice=stop_price,
                    timeInForce='GTC'
                )
            else:
                order = None
            result = order
        except Exception as e:
            error = f"Order failed: {e}"

    return render_template_string(HTML, result=result, error=error)

if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG) 