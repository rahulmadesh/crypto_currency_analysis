import requests
import pandas as pd
from datetime import datetime

def get_live_market_chart(coin_id="bitcoin", minutes=60):
    """
    Fetch live price movement for last N minutes
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": 1,
        "interval": "minute"
    }

    r = requests.get(url, params=params)
    data = r.json()

    prices = data.get("prices", [])

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["Date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.tail(minutes)

    return df[["Date", "price"]]
