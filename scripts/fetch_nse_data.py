import yfinance as yf
import json
import time
from datetime import datetime

# F&O stocks list
symbols = ['SBIN.NS', 'RELIANCE.NS', 'INFY.NS', 'TCS.NS', 'HDFCBANK.NS']
data = []

print("Starting data fetch...")

for symbol in symbols:
    try:
        print(f"Fetching {symbol}...")
        ticker = yf.Ticker(symbol)
        
        # Spot price nikaal
        hist = ticker.history(period="1d")
        if hist.empty:
            print(f"No data for {symbol}")
            continue
            
        spot = round(hist['Close'].iloc[-1], 2)
        
        # Futures ka data Yahoo pe nahi milta, to basic version me dummy daal rahe
        # Real futures ke liye Dhan API hi lagega
        curr_fut = round(spot * 1.018, 2)  # 1.8% premium dummy
        next_fut = round(spot * 1.019, 2)  # 1.9% premium dummy
        
        data.append({
            'symbol': symbol.replace('.NS', ''),
            'spot': spot,
            'currFut': curr_fut,
            'nextFut': next_fut,
            'diffSpotFut': round((curr_fut - spot) / spot * 100, 2),
            'diffFutFut': round((next_fut - curr_fut) / curr_fut * 100, 2),
            'timestamp': str(datetime.now())
        })
        print(f"Success: {symbol} Spot={spot}")
        
    except Exception as e:
        print(f"Error {symbol}: {e}")
    
    time.sleep(1) # Yahoo rate limit

print(f"Total fetched: {len(data)}")
with open('data/futures_data.json', 'w') as f:
    json.dump(data, f, indent=2)
print("JSON saved")
