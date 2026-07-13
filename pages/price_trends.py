import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def run(df):
    st.title("📈 Price Trend & Market Structure Analysis")

    data = df.tail(200).copy()

    # ===============================
    # TECHNICAL INDICATORS
    # ===============================
    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()
    data["AvgVolume"] = data["Volume"].rolling(20).mean()

    last_close = data["Close"].iloc[-1]
    prev_close = data["Close"].iloc[-2]
    ma20 = data["MA20"].iloc[-1]
    ma50 = data["MA50"].iloc[-1]
    last_volume = data["Volume"].iloc[-1]
    avg_volume = data["AvgVolume"].iloc[-1]

    price_change = last_close - prev_close

    # ===============================
    # PRICE TREND LOGIC
    # ===============================
    if last_close > ma20 > ma50:
        price_trend = "Bullish 📈"
    elif last_close < ma20 < ma50:
        price_trend = "Bearish 📉"
    else:
        price_trend = "Sideways ➖"

    # ===============================
    # VOLUME CONFIRMATION
    # ===============================
    if last_volume > avg_volume * 1.25:
        volume_state = "High Volume"
    else:
        volume_state = "Normal Volume"

    # ===============================
    # TREND CONFIRMATION
    # ===============================
    if price_trend == "Bullish 📈" and volume_state == "High Volume":
        trend_strength = "Strong Uptrend ✅"
        market_phase = "Confirmed breakout with strong buying interest"
    elif price_trend == "Bearish 📉" and volume_state == "High Volume":
        trend_strength = "Strong Downtrend ⚠️"
        market_phase = "Confirmed sell-off with strong distribution"
    elif price_trend != "Sideways ➖":
        trend_strength = "Weak / Unconfirmed"
        market_phase = "Price moving without volume confirmation"
    else:
        trend_strength = "Range-Bound"
        market_phase = "Market consolidation phase"

    # ===============================
    # KPI CARDS
    # ===============================
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Latest Price", f"${last_close:,.2f}")
    c2.metric("Price Trend", price_trend)
    c3.metric("Trend Strength", trend_strength)
    c4.metric("Market Phase", market_phase)

    st.markdown("---")

    # ===============================
    # PRICE + MA + VOLUME CHART
    # ===============================
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=data["Date"],
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="Price"
    ))

    fig.add_trace(go.Scatter(
        x=data["Date"],
        y=data["MA20"],
        name="MA 20",
        line=dict(color="#00d4ff", width=2)
    ))

    fig.add_trace(go.Scatter(
        x=data["Date"],
        y=data["MA50"],
        name="MA 50",
        line=dict(color="#f59e0b", width=2)
    ))

    fig.update_layout(
        title="Bitcoin Price Trend with Volume-Confirmed Structure",
        template="plotly_dark",
        height=520,
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # INTERPRETATION
    # ===============================
    st.subheader("📖 Professional Interpretation")

    st.write(f"""
    - The market is currently **{price_trend}**.
    - Volume conditions indicate **{volume_state.lower()}**, which
      makes the trend **{trend_strength.lower()}**.
    - This context is critical when validating **ARIMA, SARIMA, LSTM, and Prophet forecasts**.
    - Forecasts aligned with **confirmed trends** have higher reliability.
    """)
