import streamlit as st
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from datetime import timedelta
import numpy as np   # NEW

def run(df):
    st.title("🤖 ARIMA Forecasting")

    series = df["Close"].values[-500:]
    model = ARIMA(series, order=(5,1,0))
    fitted = model.fit()

    forecast = fitted.forecast(steps=30)
    future_dates = [
        df["Date"].iloc[-1] + timedelta(days=i) for i in range(1, 31)
    ]

    # ===============================
    # CONFIDENCE CALCULATION (NEW)
    # ===============================
    fitted_values = fitted.fittedvalues
    actual_values = series[-len(fitted_values):]

    rmse = np.sqrt(np.mean((actual_values - fitted_values) ** 2))
    last_price = series[-1]

    arima_confidence = max(0, 100 - (rmse / last_price) * 100)
    arima_confidence = round(arima_confidence, 2)

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
        name="ARIMA Forecast",
        line=dict(dash="dash")
    ))

    st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # FUTURE PRICE TREND SUMMARY
    # ===============================
    st.subheader("📊 Future Price Trend Summary")

    predicted_price = forecast[-1]

    if predicted_price > last_price * 1.002:
        arima_trend = "Bullish 📈"
        interpretation = "Statistical upward momentum detected"
    elif predicted_price < last_price * 0.998:
        arima_trend = "Bearish 📉"
        interpretation = "Statistical downward pressure detected"
    else:
        arima_trend = "Sideways ➖"
        interpretation = "Price expected to remain stable"

    import pandas as pd

    trend_table = pd.DataFrame({
        "Metric": [
            "Model Used",
            "Last Actual Price (USD)",
            "Predicted Price (USD)",
            "Trend Direction",
            "Model Confidence (%)",
            "Interpretation"
        ],
        "Value": [
            "ARIMA",
            f"${last_price:,.2f}",
            f"${predicted_price:,.2f}",
            arima_trend,
            f"{arima_confidence}%",
            interpretation
        ]
    })

    st.dataframe(trend_table, use_container_width=True)

    # ===============================
    # NEXT 30 DAYS ARIMA PREDICTION
    # ===============================
    st.subheader("📅 Next 30 Days Price Forecast (ARIMA)")

    arima_table = pd.DataFrame({
        "Date": future_dates,
        "Predicted Price (USD)": forecast.round(2)
    })

    st.dataframe(arima_table, use_container_width=True)
    st.session_state["ARIMA_CONF"] = arima_confidence


