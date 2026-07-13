import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def run(df):
    st.title("📊 Volume, Participation & Trend Confirmation")

    data = df.tail(200).copy()
    data["AvgVolume"] = data["Volume"].rolling(20).mean()

    last_volume = data["Volume"].iloc[-1]
    avg_volume = data["AvgVolume"].iloc[-1]
    price_change = data["Close"].iloc[-1] - data["Close"].iloc[-2]

    # ===============================
    # VOLUME BEHAVIOR LOGIC
    # ===============================
    if last_volume > avg_volume * 1.3 and price_change > 0:
        volume_signal = "Accumulation 🟢"
        meaning = "Buyers are aggressively entering the market"
    elif last_volume > avg_volume * 1.3 and price_change < 0:
        volume_signal = "Distribution 🔴"
        meaning = "Large sell-off confirming bearish pressure"
    elif last_volume < avg_volume * 0.7:
        volume_signal = "Low Participation ⚪"
        meaning = "Weak conviction, trends may fail"
    else:
        volume_signal = "Neutral Activity 🟡"
        meaning = "Balanced participation"

    # ===============================
    # KPI CARDS
    # ===============================
    c1, c2, c3 = st.columns(3)

    c1.metric("Latest Volume", f"{last_volume:,.0f}")
    c2.metric("Volume Signal", volume_signal)
    c3.metric("Market Meaning", meaning)

    st.markdown("---")

    # ===============================
    # VOLUME CHART
    # ===============================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=data["Date"],
        y=data["Volume"],
        name="Daily Volume",
        marker_color="#374151"
    ))

    fig.add_trace(go.Scatter(
        x=data["Date"],
        y=data["AvgVolume"],
        name="20-Day Avg Volume",
        line=dict(color="#f59e0b", width=2)
    ))

    fig.update_layout(
        title="Bitcoin Volume & Market Participation",
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # INTERPRETATION
    # ===============================
    st.subheader("📖 Professional Interpretation")

    st.write(f"""
    - Current volume behavior suggests **{volume_signal.lower()}**.
    - Volume confirms whether **price movements are trustworthy**.
    - High volume strengthens forecast confidence.
    - Low participation warns of **false breakouts or unreliable predictions**.
    """)
