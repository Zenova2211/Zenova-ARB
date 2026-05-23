import requests
import json
import time
import sys

# Test ke liye sirf 3 stocks. Baad me list badhana
symbols = ['SBIN', 'RELIANCE', 'INFY']

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nseindia.com/market-data/live-equity-market',
    'Connection': 'keep-alive'
}

print("Hitting NSE homepage first...")
try:
    session.get("https://www.nseindia.com", headers=headers, timeout=5)
    print("Homepage OK")
except Exception as e:
    print(f"Homepage failed: {e}")
    sys.exit(1)

time.sleep(2)
data = []

for symbol in symbols:
    print(f"Fetching {symbol}...")
    try:
        url = f"https://www.nseindia.com/api/quote-derivative?symbol={symbol}"
        r = session.get(url, headers=headers, timeout=5)
        print(f"Status for {symbol}: {r.status_code}")

        if r.status_code == 200:
            d = r.json()
            stocks = d.get('stocks', [])
            if d.get('underlyingValue') and len(stocks) >= 2:
                spot = d['underlyingValue']
                currFut = stocks[0]['metadata']['lastPrice']
                nextFut = stocks[1]['metadata']['lastPrice']
                data.append({
                    'symbol': symbol,
                    'spot': spot,
                    'currFut': currFut,
                    'nextFut': nextFut,
                    'diffSpotFut': round((currFut - spot) / spot * 100, 2),
                    'diffFutFut': round((nextFut - currFut) / currFut * 100, 2),
                })
                print(f"Success: {symbol}")
        else:
            print(f"Failed {symbol}: {r.text[:100]}")

    except Exception as e:
        print(f"Error {symbol}: {e}")

    time.sleep(1) # Rate limit avoid

print(f"Total fetched: {len(data)}")
with open('data/futures_data.json', 'w') as f:
    json.dump(data, f, indent=2)
print("JSON saved")
