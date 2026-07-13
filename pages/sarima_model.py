import streamlit as st
import plotly.graph_objects as go
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta
import numpy as np   # NEW

def run(df):
    st.title("📐 SARIMA Forecasting")

    series = df["Close"].values[-500:]

    model = SARIMAX(
        series,
        order=(1,1,1),
        seasonal_order=(1,1,1,12)
    )
    fitted = model.fit(disp=False)

    forecast = fitted.forecast(steps=30)
    future_dates = [
        df["Date"].iloc[-1] + timedelta(days=i) for i in range(1, 31)
    ]

    # ===============================
    # CONFIDENCE CALCULATION (NEW)
    # ===============================
    residuals = fitted.resid
    last_price = series[-1]

    seasonal_volatility = np.std(residuals)
    sarima_confidence = max(0, 100 - (seasonal_volatility / last_price) * 100)
    sarima_confidence = round(sarima_confidence, 2)

    # ===============================
    # GRAPH
    # ===============================
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Date"].tail(100),
        y=df["Close"].tail(100),
        name="Historical Price"
    ))
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=forecast,
        name="SARIMA Forecast",
        line=dict(dash="dot")
    ))

    st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # FUTURE PRICE TREND SUMMARY
    # ===============================
    st.markdown("<div class='section-title'>📊 Future Price Trend Summary</div>", unsafe_allow_html=True)

    import pandas as pd

    predicted_price = forecast[-1]

    if predicted_price > last_price * 1.002:
        sarima_trend = "Bullish 📈"
    elif predicted_price < last_price * 0.998:
        sarima_trend = "Bearish 📉"
    else:
        sarima_trend = "Sideways ➖"

    trend_table = pd.DataFrame({
        "Metric": [
            "Model Used",
            "Last Actual Price (USD)",
            "Predicted Price (USD)",
            "Trend Direction",
            "Model Confidence (%)"
        ],
        "Value": [
            "SARIMA",
            f"${last_price:,.2f}",
            f"${predicted_price:,.2f}",
            sarima_trend,
            f"{sarima_confidence}%"
        ]
    })

    st.dataframe(trend_table, use_container_width=True)

    # ===============================
    # NEXT 30 DAYS SARIMA PREDICTION
    # ===============================
    st.subheader("📅 Next 30 Days Price Forecast (SARIMA)")

    sarima_table = pd.DataFrame({
        "Date": future_dates,
        "Predicted Price (USD)": forecast.round(2)
    })

    st.dataframe(sarima_table, use_container_width=True)
    st.session_state["SARIMA_CONF"] = sarima_confidence
