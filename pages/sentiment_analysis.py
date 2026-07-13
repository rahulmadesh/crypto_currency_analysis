import streamlit as st
import requests
import pandas as pd
from textblob import TextBlob

# ===============================
# REAL-WORLD CRYPTO SENTIMENT
# ===============================

NEWS_API_KEY = "57fe47fc0a6649f6ad44e64115923788"

def fetch_crypto_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "bitcoin OR cryptocurrency",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    articles = data.get("articles", [])
    headlines = [a["title"] for a in articles if a["title"]]
    return headlines

def get_average_sentiment():
    headlines = fetch_crypto_news()

    if len(headlines) == 0:
        return 0, pd.DataFrame()

    scores = []
    for text in headlines:
        polarity = TextBlob(text).sentiment.polarity
        scores.append(polarity)

    df = pd.DataFrame({
        "News Headline": headlines,
        "Sentiment Score": scores
    })

    avg_sentiment = sum(scores) / len(scores)
    return avg_sentiment, df


def run(df):
    st.title("📰 Market Sentiment Intelligence")
    st.caption("Real-time cryptocurrency news sentiment analysis")

    avg_sentiment, sentiment_df = get_average_sentiment()

    # ===============================
    # KPI CARDS
    # ===============================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("News Articles Analyzed", len(sentiment_df))

    with col2:
        st.metric("Average Sentiment Score", round(avg_sentiment, 3))

    with col3:
        if avg_sentiment > 0.05:
            st.success("📈 Market Mood: Positive")
        elif avg_sentiment < -0.05:
            st.error("📉 Market Mood: Negative")
        else:
            st.warning("➖ Market Mood: Neutral")

    st.markdown("---")
    st.markdown("""
<style>

/* Global text */
html, body, [class*="css"]  {
    color: #ffffff !important;
}

/* Section titles */
h1, h2, h3, h4 {
    color: #ffffff !important;
}

/* KPI numbers */
.metric-value {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* Dataframe headers */
thead tr th {
    background-color: #1f2933 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Dataframe cells */
tbody tr td {
    background-color: #111827 !important;
    color: #e5e7eb !important;
}

/* Streamlit metric labels */
[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}

/* Streamlit metric values */
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}

/* Sentiment badge */
.sentiment-box {
    background: #065f46;
    color: #ecfdf5;
    padding: 12px 18px;
    border-radius: 12px;
    font-weight: 600;
    display: inline-block;
}

</style>
""", unsafe_allow_html=True)


    # ===============================
    # SENTIMENT TABLE
    # ===============================
    st.subheader("🗞 Latest Crypto News & Sentiment")
    st.dataframe(sentiment_df)

    st.markdown("---")

    # ===============================
    # INTERPRETATION
    # ===============================
    st.subheader("📖 Interpretation")
    st.write("""
    This module analyzes real-world cryptocurrency news using Natural Language
    Processing (NLP). Positive sentiment reflects optimistic market expectations,
    while negative sentiment indicates fear or uncertainty. These insights help
    contextualize price trends and forecasting models.
    """)
