import streamlit as st
import plotly.express as px

def run(df):
    st.title("⚠️ Volatility & Risk Analysis")

    df["Returns"] = df["Close"].pct_change()
    df["Volatility"] = df["Returns"].rolling(30).std()

    fig = px.line(df, x="Date", y="Volatility",
                  title="30-Day Rolling Volatility")
    st.plotly_chart(fig, use_container_width=True)

    st.write(
        "Higher volatility indicates increased market risk and uncertainty."
    )
