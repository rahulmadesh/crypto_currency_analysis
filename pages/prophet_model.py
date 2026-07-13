import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from prophet import Prophet
from streamlit_autorefresh import st_autorefresh

# ===============================
# AUTO REFRESH
# ===============================
st_autorefresh(interval=60 * 1000, key="prophet_refresh")

# ===============================
# UI STYLING (SAME AS OTHERS)
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
    st.markdown("<div class='section-title'>📊 Trend & Seasonality Forecasting (Facebook Prophet)</div>", unsafe_allow_html=True)
    st.caption("Medium-term Bitcoin price forecasting using Facebook Prophet")

    # ===============================
    # DATA PREP FOR PROPHET
    # ===============================
    prophet_df = df[["Date", "Close"]].rename(columns={
        "Date": "ds",
        "Close": "y"
    })

    # ===============================
    # PROPHET MODEL
    # ===============================
    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=True,
        changepoint_prior_scale=0.05
    )

    model.fit(prophet_df)

    # ===============================
    # FUTURE FORECAST
    # ===============================
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    last_price = prophet_df["y"].iloc[-1]
    predicted_price = forecast["yhat"].iloc[-1]

    # ===============================
    # TREND DIRECTION
    # ===============================
    if predicted_price > last_price * 1.002:
        prophet_trend = "Bullish 📈"
    elif predicted_price < last_price * 0.998:
        prophet_trend = "Bearish 📉"
    else:
        prophet_trend = "Sideways ➖"

    # ===============================
    # CONFIDENCE SCORE (STABILITY-BASED)
    # ===============================
    uncertainty = forecast["yhat_upper"].iloc[-1] - forecast["yhat_lower"].iloc[-1]
    prophet_confidence = max(0, 100 - (uncertainty / last_price) * 100)
    prophet_confidence = round(prophet_confidence, 2)

    # ===============================
    # KPI CARDS
    # ===============================
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">LIVE BTC PRICE</div>
            <div class="kpi-value">${last_price:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">PROPHET TREND</div>
            <div class="kpi-value">{prophet_trend}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">CONFIDENCE</div>
            <div class="kpi-value">{prophet_confidence}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ===============================
    # FORECAST GRAPH
    # ===============================
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=prophet_df["ds"].tail(120),
        y=prophet_df["y"].tail(120),
        name="Historical Price"
    ))

    fig.add_trace(go.Scatter(
        x=forecast["ds"].tail(30),
        y=forecast["yhat"].tail(30),
        name="Prophet Forecast"
    ))

    fig.add_trace(go.Scatter(
        x=forecast["ds"].tail(30),
        y=forecast["yhat_upper"].tail(30),
        fill=None,
        mode="lines",
        line=dict(width=0),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=forecast["ds"].tail(30),
        y=forecast["yhat_lower"].tail(30),
        fill="tonexty",
        name="Confidence Band",
        opacity=0.3
    ))

    fig.update_layout(
        title="Bitcoin Price Forecast (Facebook Prophet)",
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # FUTURE PRICE TABLE
    # ===============================
    st.subheader("📋 Next 30 Days Forecast (Prophet)")

    table = forecast.tail(30)[["ds", "yhat"]].rename(columns={
        "ds": "Date",
        "yhat": "Predicted Price (USD)"
    })

    table["Predicted Price (USD)"] = table["Predicted Price (USD)"].round(2)

    st.dataframe(table, use_container_width=True)

    # ===============================
    # INTERPRETATION
    # ===============================
    st.markdown("<div class='section-title'>📖 Interpretation</div>", unsafe_allow_html=True)
    st.write("""
    Facebook Prophet models Bitcoin prices by decomposing the time series into
    **trend**, **seasonality**, and **noise** components. This makes Prophet highly
    suitable for volatile financial data and provides transparent, interpretable
    forecasts compared to black-box models.
    """)
    st.session_state["PROPHET_CONF"] = prophet_confidence
