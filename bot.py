import ccxt
import os
from flask import Flask, request

app = Flask(__name__)

api_key = os.environ['API_KEY']
secret = os.environ['API_SECRET']

exchange = ccxt.bitflyer({
    'apiKey': api_key,
    'secret': secret,
})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data['action'] == 'buy':
        order = exchange.create_market_buy_order('BTC/JPY', 0.01)
        return f"Bought 0.01 BTC at market price"
    elif data['action'] == 'sell':
        order = exchange.create_market_sell_order('BTC/JPY', 0.01)
        return f"Sold 0.01 BTC at market price"
    return 'Invalid action', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
