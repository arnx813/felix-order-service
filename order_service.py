from flask import Flask, request, jsonify
from hyperliquid.exchange import Exchange
from eth_account import Account
import traceback

# Initialize Flask app
app = Flask(__name__)

# API credentials
API_URL = "https://api.hyperliquid.xyz"
PRIVATE_KEY = "0x5d227724c508cfc97e95b84916dd6c6dde7200c6641c9b5024e97ec1c44839b6"  # Replace with actual private key
exchange = Exchange(Account.from_key(PRIVATE_KEY), API_URL)

def open_spot_market_order(symbol, is_buy, quantity):
    """
    Place a market spot order on the exchange.
    """
    try:
        # Create the order
        order_result = exchange.market_open(symbol, is_buy, quantity, None, 0.01)
        # order_result = exchange.market_open("PURR/USDC", True, 100, None, 0.01)

        # Check and return the result
        if order_result["status"] == "ok":
            return order_result
        else:
            raise Exception(f"Market order failed: {order_result}")
    except Exception as e:
        print(f"Error placing order: {e}")
        traceback.print_exc()
        return {"error": str(e)}

@app.route("/market-order", methods=["POST"])
def market_order():
    """
    Endpoint to trigger a market order.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request, JSON body required"}), 400

    try:
        # Extract parameters from the request
        symbol = data.get("symbol")
        is_buy = data.get("is_buy")
        quantity = data.get("quantity")

        if not symbol or is_buy is None or not quantity:
            return jsonify({"error": "Missing required fields: symbol, is_buy, quantity"}), 400

        # Trigger the market order
        result = open_spot_market_order(symbol, is_buy, quantity)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
