import requests
import json
import pandas as pd
from datetime import datetime

# NSE F&O symbols
symbols = ["360ONE","ABB","ABCAPITAL","ADANIENT","ADANIENSOL","ADANIGREEN","ADANIPORTS","ADANIPOWER",
    "ALKEM","AMBER","AMBUJACEM","ANGELONE","APLAPOLLO","APOLLOHOSP","ASHOKLEY","ASIANPAINT",
    "ASTRAL","AUBANK","AUROPHARMA","AXISBANK",
    "BAJAJ-AUTO","BAJAJFINSV","BAJAJHLDNG","BAJFINANCE","BANDHANBNK","BANKINDIA","BANKBARODA",
    "BDL","BEL","BHARATFORG","BHARTIARTL","BHEL","BIOCON","BLUESTARCO","BOSCHLTD","BPCL",
    "BRITANNIA","BSE",
    "CAMS","CANBK","CDSL","CGPOWER","CHOLAFIN","CIPLA","COALINDIA","COCHINSHIP","COFORGE",
    "COLPAL","CONCOR","CROMPTON","CUMMINSIND",
    "DABUR","DALBHARAT","DELHIVERY","DIVISLAB","DIXON","DLF","DMART","DRREDDY",
    "EICHERMOT","ETERNAL","EXIDEIND",
    "FEDERALBNK","FORCEMOT","FORTIS",
    "GAIL","GLENMARK","GMRAIRPORT","GODREJCP","GODREJPROP","GODFRYPHLP","GRASIM",
    "HAL","HAVELLS","HCLTECH","HDFCAMC","HDFCBANK","HDFCLIFE","HEROMOTOCO","HINDALCO",
    "HINDPETRO","HINDUNILVR","HINDZINC","HUDCO","HYUNDAI",
    "ICICIBANK","ICICIGI","ICICIPRULI","IDFCFIRSTB","IDEA","IEX","INDHOTEL","INDIGO",
    "INDIANB","INDUSTOWER","INFY","INOXWIND","IOC","IREDA","IRFC","ITC",
    "JINDALSTEL","JIOFIN","JUBLFOOD","JSWENERGY","JSWSTEEL",
    "KALYANKJIL","KAYNES","KEI","KFINTECH","KOTAKBANK","KPITTECH",
    "LAURUSLABS","LICHSGFIN","LICI","LODHA","LT","LTF","LTM","LUPIN",
    "M&M","MANKIND","MANAPPURAM","MARICO","MARUTI","MAXHEALTH","MAZDOCK","MCX","MFSL",
    "MOTHERSON","MOTILALOFS","MPHASIS","MUTHOOTFIN",
    "NAM-INDIA","NATIONALUM","NAUKRI","NBCC","NESTLEIND","NHPC","NMDC","NTPC","NUVAMA","NYKAA",
    "OBEROIRLTY","OFSS","OIL","ONGC",
    "PAGEIND","PATANJALI","PAYTM","PFC","PETRONET","PHOENIXLTD","PIDILITIND","PIIND",
    "PNBHOUSING","POLICYBZR","POLYCAB","POWERGRID","POWERINDIA","PREMIERENE","PRESTIGE",
    "PNB","PPLPHARMA","PERSISTENT",
    "RBLBANK","RECLTD","RELIANCE","RVNL",
    "SAIL","SAMMAANCAP","SBICARD","SBILIFE","SBIN","SHREECEM","SHRIRAMFIN","SIEMENS",
    "SOLARINDS","SONACOMS","SRF","SUPREMEIND","SUZLON","SWIGGY",
    "TATACONSUM","TATAELXSI","TATAPOWER","TATASTEEL","TATATECH","TCS","TECHM","TIINDIA",
    "TITAN","TMPV","TORNTPHARM","TORNTPOWER","TRENT","TVSMOTOR",
    "ULTRACEMCO","UNIONBANK","UNITDSPR","UNOMINDA","UPL",
    "VBL","VEDL","VMM","VOLTAS",
    "WAAREEENER","WIPRO",
    "YESBANK",
    "ZYDUSLIFE",
    "PGEL","JSWENERGY","PAYTM","JIOFIN","ETERNAL","KAYNES","CGPOWER","ANGELONE","BSE",
    "CAMS","CDSL","KFINTECH","NUVAMA","MOTILALOFS","NAM-INDIA","HYUNDAI","COCHINSHIP",
    "FORCEMOT","GODFRYPHLP","ADANIPOWER","VMM",] # Add all F&O stocks

data = []
for symbol in symbols:
    try:
        # NSE API endpoint
        url = f"https://www.nseindia.com/api/quote-derivative?symbol={symbol}"
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            d = response.json()
            data.append({
                'symbol': symbol,
                'spot': d['underlyingValue'],
                'currFut': d['futures'][0]['lastPrice'],
                'nextFut': d['futures'][1]['lastPrice'],
                'diffSpotFut': (d['futures'][0]['lastPrice'] - d['underlyingValue']) / d['underlyingValue'] * 100,
                'diffFutFut': (d['futures'][1]['lastPrice'] - d['futures'][0]['lastPrice']) / d['futures'][0]['lastPrice'] * 100,
            })
    except Exception as e:
        print(f"Error {symbol}: {e}")

# Save to JSON
with open('data/futures_data.json', 'w') as f:
    json.dump(data, f, indent=2)
