import pandas as pd
import requests
from datetime import datetime

# -------------------------------
# Fetch live crypto price
# -------------------------------
def get_live_price(crypto="bitcoin"):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": crypto,
        "vs_currencies": "usd"
    }

    response = requests.get(url, params=params)
    data = response.json()

    price = data[crypto]["usd"]

    return {
        "Date": datetime.now(),
        "Open": price,
        "High": price,
        "Low": price,
        "Close": price,
        "Volume": 0
    }

# -------------------------------
# Load historical + live data
# -------------------------------
def load_data(crypto="Bitcoin", include_live=True):
    """
    crypto: 'Bitcoin' or 'Ethereum'
    """

    # ===============================
    # LOAD HISTORICAL DATA
    # ===============================
    if crypto == "Bitcoin":
        df = pd.read_csv("bitcoin_history.csv")

    elif crypto == "Ethereum":
        df = pd.read_csv("coin_Ethereum.csv")

        # ---- STANDARDIZE ETH COLUMNS ----
        df.columns = df.columns.str.lower().str.strip()
        df = df.rename(columns={
            "date": "Date",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume"
        })

    else:
        raise ValueError("Unsupported cryptocurrency")

    # ===============================
    # COMMON CLEANING (BTC + ETH)
    # ===============================
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    # ===============================
    # ADD LIVE PRICE
    # ===============================
    if include_live:
        if crypto == "Bitcoin":
            live_row = get_live_price("bitcoin")
        else:
            live_row = get_live_price("ethereum")

        live_df = pd.DataFrame([live_row])
        df = pd.concat([df, live_df], ignore_index=True)

    return df
