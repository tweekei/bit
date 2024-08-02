import ccxt
import os
import time
from threading import Thread
from flask import Flask, request

app = Flask(__name__)

api_key = os.environ['API_KEY']
secret = os.environ['API_SECRET']

exchange = ccxt.bitflyer({
    'apiKey': api_key,
    'secret': secret,
})

def execute_trade(action, amount, hold_time):
    if action == 'buy':
        order = exchange.create_market_buy_order('BTC/JPY', amount)
        print(f"Bought {amount} BTC at market price")
        time.sleep(hold_time)  # Wait for the specified hold time
        sell_order = exchange.create_market_sell_order('BTC/JPY', amount)
        print(f"Sold {amount} BTC at market price after holding for {hold_time} seconds")
    elif action == 'sell':
        order = exchange.create_market_sell_order('BTC/JPY', amount)
        print(f"Sold {amount} BTC at market price")
    else:
        print('Invalid action')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    action = data.get('action')
    amount = data.get('amount')
    hold_time = data.get('hold_time', 0)  # Default to 0 if not provided

    if action and amount:
        # Execute the trade in a separate thread to avoid blocking the webhook response
        Thread(target=execute_trade, args=(action, amount, hold_time)).start()
        return f"Received {action} action for {amount} BTC"
    else:
        return 'Invalid request', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))