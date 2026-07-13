import streamlit as st
from data_loader import load_data

# ===== PAGE CONFIG (ONLY ONCE, AT TOP) =====
st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide"
)

# ===== GLOBAL DASHBOARD THEME =====
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Dashboard cards */
.dashboard-card {
    background-color: #1f2937;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    text-align: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
st.sidebar.title("Crypto Market")

# ===============================
# ✅ ADDED: CRYPTO SELECTION
# ===============================
crypto = st.sidebar.selectbox(
    "Select Cryptocurrency",
    ["Bitcoin", "Ethereum"]
)

# ===============================
# LOAD DATA (UPDATED CALL)
# ===============================
df = load_data(crypto=crypto, include_live=True)

# ===== PAGE ROUTING =====
pages = {
    "📊 Market Overview": "pages.executive_summary",
    "📉 Price Action": "pages.price_trends",
    "📦 Liquidity & Volume": "pages.volume_analysis",
    "🤖 ARIMA Forecasting": "pages.arima_model",
    "📊 Seasonal Forecasting (SARIMA)": "pages.sarima_model",
    "🧠 AI Price Prediction (LSTM)": "pages.lstm_model",
    "⚠️ Risk & Volatility": "pages.volatility_risk",
    "📰 Market Sentiment Intelligence": "pages.sentiment_analysis",
    "📊 Prophet Forecasting": "pages.prophet_model",
    "📊 Model Confidence": "pages.model_confidence",
    "✅ Strategic Insights": "pages.final_conclusion",
}

choice = st.sidebar.selectbox("Select Dashboard Module", list(pages.keys()))

module = __import__(pages[choice], fromlist=["run"])

if choice == "📊 Model Confidence":
    confidence_data = {
        "ARIMA": st.session_state.get("ARIMA_CONF", 0),
        "SARIMA": st.session_state.get("SARIMA_CONF", 0),
        "LSTM": st.session_state.get("LSTM_CONF", 0),
        "PROPHET": st.session_state.get("PROPHET_CONF", 0)
    }
    module.run(confidence_data)
else:
    module.run(df)
