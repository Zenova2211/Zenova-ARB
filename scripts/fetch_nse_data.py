import requests
import json
import time
from datetime import datetime

# F&O stocks with NSE suffix for Yahoo
symbols = ['SBIN.NS', 'RELIANCE.NS', 'INFY.NS', 'TCS.NS', 'HDFCBANK.NS']
data = []

def get_yahoo_data(symbol):
    try:
        # Spot price
        spot_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        r = requests.get(spot_url, timeout=10)
        spot = r.json()['chart']['result'][0]['meta']['regularMarketPrice']

        # Futures - Yahoo me direct nahi milta, isliye NSE se hi try karna padega
        # Abhi ke liye dummy data daal rahe, Dhan API aane pe real karenge
        curr_fut = spot * 1.018 # 1.8% premium maan ke
        next_fut = spot * 1.019

        return {
            'symbol': symbol.replace('.NS', ''),
            'spot': round(spot, 2),
            'currFut': round(curr_fut, 2),
            'nextFut': round(next_fut, 2),
            'diffSpotFut': round((curr_fut - spot) / spot * 100, 2),
            'diffFutFut': round((next_fut - curr_fut) / curr_fut * 100, 2),
            'timestamp': str(datetime.now())
        }
    except Exception as e:
        print(f"Error {symbol}: {e}")
        return None

for symbol in symbols:
    print(f"Fetching {symbol}...")
    result = get_yahoo_data(symbol)
    if result:
        data.append(result)
        print(f"Done: {symbol}")
    time.sleep(1)

print(f"Total fetched: {len(data)}")
with open('data/futures_data.json', 'w') as f:
    json.dump(data, f, indent=2)
print("JSON saved")
