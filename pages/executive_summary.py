import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# ======================
# AUTO REFRESH (10 SEC)
# ======================
st_autorefresh(interval=10 * 1000, key="live_refresh_exec")

# ======================
# LIVE OHLC DATA (API)
# ======================
def get_live_ohlc(coin_id="bitcoin", points=60):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
    params = {
        "vs_currency": "usd",
        "days": 1
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    df = pd.DataFrame(
        data,
        columns=["timestamp", "open", "high", "low", "close"]
    )
    df["Date"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df.tail(points)


def run(df):
    # ======================
    # PAGE TITLE
    # ======================
    st.title("🚀 Crypto Market Intelligence Dashboard")
    st.caption("🔴 Near real-time market data (auto-refresh every 10 sec)")

    # ======================
    # DASHBOARD CARDS
    # ======================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="dashboard-card">
            <h3>💰 Live BTC Price</h3>
            <h2>${df['Close'].iloc[-1]:,.2f}</h2>
            <small>{df['Date'].iloc[-1]}</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="dashboard-card">
            <h3>📊 Total Records</h3>
            <h2>{len(df)}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <h3>📈 Market Status</h3>
            <h2>Active</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ======================
    # LONG-TERM PRICE CHART
    # ======================
    st.subheader("📉 Bitcoin Price Trend (Long Term)")
    fig_long = px.line(df, x="Date", y="Close")
    fig_long.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_long, use_container_width=True)

    st.markdown("---")

    # ======================
    # 🔴 LIVE CANDLESTICK GRAPH
    # ======================
    st.subheader("⚡ Live Price Movement (Green / Red Candles)")

    ohlc_df = get_live_ohlc("bitcoin", points=60)

    if ohlc_df.empty:
        st.warning("Waiting for live market data…")
        return

    fig_live = go.Figure(data=[
        go.Candlestick(
            x=ohlc_df["Date"],
            open=ohlc_df["open"],
            high=ohlc_df["high"],
            low=ohlc_df["low"],
            close=ohlc_df["close"],
            increasing_line_color="#00C853",
            decreasing_line_color="#D50000",
            name="BTC/USD"
        )
    ])

    fig_live.update_layout(
        template="plotly_dark",
        height=420,
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig_live, use_container_width=True)

    st.markdown("---")

    # ======================
    # MODULE NAVIGATION
    # ======================
    st.subheader("🧭 Explore Modules")

    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button("📈 Price Trends"):
            st.session_state.selected_page = "📉 Price Action"
            st.rerun()

    with b2:
        if st.button("🤖 Forecast Models"):
            st.session_state.selected_page = "🤖 ARIMA Forecasting"
            st.rerun()

    with b3:
        if st.button("📰 Sentiment Analysis"):
            st.session_state.selected_page = "📰 Market Sentiment Intelligence"
            st.rerun()
