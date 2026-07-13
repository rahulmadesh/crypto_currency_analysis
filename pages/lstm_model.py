import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from streamlit_autorefresh import st_autorefresh

from pages.sentiment_analysis import get_average_sentiment

# ===============================
# AUTO REFRESH
# ===============================
st_autorefresh(interval=60 * 1000, key="lstm_trend_refresh")

# ===============================
# UI STYLING
# ===============================
st.markdown("""
<style>
.kpi-card {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    color: white;
}
.kpi-title { font-size: 14px; color: #e5e7eb; }
.kpi-value { font-size: 26px; font-weight: bold; }
.section-title { font-size: 22px; color: white; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


def run(df):
    st.markdown("<div class='section-title'>🧠 AI Future Trend Prediction (LSTM)</div>", unsafe_allow_html=True)
    st.caption("Trend-based future price projection using LSTM and market sentiment")

    # ===============================
    # DATA PREP
    # ===============================
    prices = df["Close"].values
    returns = np.diff(prices) / prices[:-1]

    trend_labels = []
    for r in returns:
        if r > 0.003:
            trend_labels.append(2)
        elif r < -0.003:
            trend_labels.append(0)
        else:
            trend_labels.append(1)

    scaler = MinMaxScaler()
    scaled_prices = scaler.fit_transform(prices.reshape(-1, 1))

    X, y = [], []
    window = 60

    for i in range(window, len(trend_labels)):
        X.append(scaled_prices[i-window:i])
        y.append(trend_labels[i])

    X = np.array(X)
    y = to_categorical(y, num_classes=3)

    # ===============================
    # LSTM TREND MODEL
    # ===============================
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(window, 1)),
        Dropout(0.3),
        LSTM(32),
        Dense(3, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.fit(X, y, epochs=15, batch_size=32, verbose=0)

    # ===============================
    # TREND PREDICTION
    # ===============================
    last_window = scaled_prices[-window:].reshape(1, window, 1)
    trend_prob = model.predict(last_window, verbose=0)[0]

    trend_map = {0: "Bearish 📉", 1: "Sideways ➖", 2: "Bullish 📈"}
    predicted_trend = trend_map[np.argmax(trend_prob)]

    # 🔹 NEW: CONFIDENCE SCORE (%)
    lstm_confidence = round(np.max(trend_prob) * 100, 2)

    # ===============================
    # SENTIMENT
    # ===============================
    avg_sentiment, _ = get_average_sentiment()

    sentiment = (
        "Positive 🟢" if avg_sentiment > 0.05 else
        "Negative 🔴" if avg_sentiment < -0.05 else
        "Neutral 🟡"
    )

    # ===============================
    # FINAL SIGNAL
    # ===============================
    if "Bullish" in predicted_trend and "Positive" in sentiment:
        final_signal = "🟢 Strong Bullish"
    elif "Bearish" in predicted_trend and "Negative" in sentiment:
        final_signal = "🔴 Strong Bearish"
    else:
        final_signal = "⚠️ Mixed / Uncertain"

    # ===============================
    # KPI CARDS
    # ===============================
    c1, c2, c3, c4, c5 = st.columns(5)  # 🔹 NEW column

    with c1:
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>LIVE BTC PRICE</div><div class='kpi-value'>${prices[-1]:,.2f}</div></div>", unsafe_allow_html=True)

    with c2:
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>LSTM TREND</div><div class='kpi-value'>{predicted_trend}</div></div>", unsafe_allow_html=True)

    with c3:
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>CONFIDENCE</div><div class='kpi-value'>{lstm_confidence}%</div></div>", unsafe_allow_html=True)

    with c4:
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>MARKET SENTIMENT</div><div class='kpi-value'>{sentiment}</div></div>", unsafe_allow_html=True)

    with c5:
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>FINAL SIGNAL</div><div class='kpi-value'>{final_signal}</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ===============================
    # TREND-BASED PRICE PROJECTION
    # ===============================
    daily_return = 0.0025 if "Bullish" in predicted_trend else -0.0025 if "Bearish" in predicted_trend else 0
    projected_prices = [prices[-1]]

    for _ in range(30):
        projected_prices.append(projected_prices[-1] * (1 + daily_return))

    projected_prices = projected_prices[1:]

    future_dates = pd.date_range(
        start=df["Date"].iloc[-1] + pd.Timedelta(days=1),
        periods=30
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"].tail(100), y=df["Close"].tail(100), name="Historical Price"))
    fig.add_trace(go.Scatter(x=future_dates, y=projected_prices, name="Trend-Based Projection"))
    fig.update_layout(title="LSTM Trend-Based Future Price Projection", template="plotly_dark", height=450)

    st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # PRICE TABLE
    # ===============================
    st.subheader("📋 Next 30 Days Projected Price List")

    table = pd.DataFrame({
        "Date": future_dates,
        "Projected Price (USD)": np.round(projected_prices, 2)
    })

    st.dataframe(table, use_container_width=True)

    # ===============================
    # INTERPRETATION
    # ===============================
    st.markdown("<div class='section-title'>📖 Interpretation</div>", unsafe_allow_html=True)
    st.write("""
    The LSTM model predicts **future price trends**, not exact prices.
    Confidence reflects the model’s certainty in the predicted trend
    based on softmax probability distribution.
    """)
    st.session_state["LSTM_CONF"] = lstm_confidence
