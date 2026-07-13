import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ===============================
# UI STYLING
# ===============================
st.markdown("""
<style>
.conf-card {
    background: linear-gradient(135deg, #1f2933, #111827);
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    color: white;
}
.conf-title {
    font-size: 14px;
    color: #9ca3af;
}
.conf-value {
    font-size: 28px;
    font-weight: bold;
}
.section-title {
    font-size: 22px;
    font-weight: 600;
    color: white;
}
</style>
""", unsafe_allow_html=True)


def run(confidence_data: dict):
    """
    confidence_data = {
        'ARIMA': 78.2,
        'SARIMA': 81.5,
        'LSTM': 64.9,
        'PROPHET': 86.1
    }
    """

    st.markdown("<div class='section-title'>📊 Unified Model Confidence Comparison</div>", unsafe_allow_html=True)
    st.caption("Comparative confidence analysis across all forecasting models")

    # ===============================
    # KPI CARDS
    # ===============================
    cols = st.columns(len(confidence_data))

    for col, (model, score) in zip(cols, confidence_data.items()):
        with col:
            st.markdown(
                f"""
                <div class="conf-card">
                    <div class="conf-title">{model}</div>
                    <div class="conf-value">{score:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ===============================
    # BAR CHART
    # ===============================
    df = pd.DataFrame({
        "Model": list(confidence_data.keys()),
        "Confidence (%)": list(confidence_data.values())
    })

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["Model"],
        y=df["Confidence (%)"],
        text=df["Confidence (%)"].round(1).astype(str) + "%",
        textposition="auto"
    ))

    fig.update_layout(
        title="Model Confidence Comparison",
        yaxis_title="Confidence (%)",
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # FINAL RECOMMENDATION
    # ===============================
    best_model = max(confidence_data, key=confidence_data.get)
    best_score = confidence_data[best_model]

    st.success(
        f"✅ **Recommended Model:** {best_model} "
        f"({best_score:.1f}% confidence)"
    )

    st.markdown("""
    **Interpretation:**  
    Higher confidence indicates stronger internal consistency and
    lower uncertainty in recent forecasts. This comparison helps
    select the most reliable model under current market conditions.
    """)
