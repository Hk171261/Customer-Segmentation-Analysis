import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

kmeans=joblib.load('kmeans_model.pkl')
scaler=joblib.load('scaler.pkl')

st.set_page_config(page_title="Customer Segment Analysis", page_icon="👥", layout="wide")

SEGMENT_INFO = {
    0: {"name": "Mature Mid-Spenders",      "color": "#639922"},
    1: {"name": "Older Digital Buyers",      "color": "#378ADD"},
    2: {"name": "Low-Income Low-Engagement", "color": "#D85A30"},
    3: {"name": "Senior High-Income Buyers", "color": "#7F77DD"},
    4: {"name": "Mid-Age Premium Buyers",    "color": "#1D9E75"},
    5: {"name": "Anomalous Profile",         "color": "#888780"},
}

CLUSTER_MEANS = {
    0: {"Age":48.6, "Income":74266,  "total_spendings":1170, "NumStorePurchases":9.1, "NumWebPurchases":4.5, "NumWebVisitsMonth":2.7, "Response":0.0},
    1: {"Age":59.5, "Income":56998,  "total_spendings":770,  "NumStorePurchases":7.5, "NumWebPurchases":7.5, "NumWebVisitsMonth":6.5, "Response":0.0},
    2: {"Age":54.0, "Income":33535,  "total_spendings":94,   "NumStorePurchases":3.1, "NumWebPurchases":2.0, "NumWebVisitsMonth":6.5, "Response":0.1},
    3: {"Age":71.3, "Income":69393,  "total_spendings":985,  "NumStorePurchases":8.1, "NumWebPurchases":4.4, "NumWebVisitsMonth":2.9, "Response":0.0},
    4: {"Age":57.9, "Income":69785,  "total_spendings":1262, "NumStorePurchases":7.2, "NumWebPurchases":5.9, "NumWebVisitsMonth":4.6, "Response":1.0},
    5: {"Age":49.0, "Income":666666, "total_spendings":62,   "NumStorePurchases":3.0, "NumWebPurchases":3.0, "NumWebVisitsMonth":6.0, "Response":0.0},
}

FEATURE_CONFIG = [
    {"key": "Age",               "label": "Age",           "max": 100,    "color": "#7F77DD", "fmt": lambda v: f"{v:.0f}"},
    {"key": "Income",            "label": "Income",        "max": 200000, "color": "#378ADD", "fmt": lambda v: f"${v:,.0f}"},
    {"key": "total_spendings",   "label": "Spending",      "max": 2000,   "color": "#1D9E75", "fmt": lambda v: f"${v:,.0f}"},
    {"key": "NumStorePurchases", "label": "Store purch.",  "max": 20,     "color": "#D85A30", "fmt": lambda v: f"{v:.0f}"},
    {"key": "NumWebPurchases",   "label": "Web purch.",    "max": 20,     "color": "#BA7517", "fmt": lambda v: f"{v:.0f}"},
    {"key": "NumWebVisitsMonth", "label": "Web visits/mo", "max": 15,     "color": "#D4537E", "fmt": lambda v: f"{v:.0f}"},
    {"key": "Response",          "label": "Recency (days)","max": 365,    "color": "#639922", "fmt": lambda v: f"{v:.0f}d"},
]

st.markdown("""
<style>
div.stButton > button {
    border: 2px solid #1D9E75;
    border-radius: 8px;
    color: #1D9E75;
    font-weight: 600;
    padding: 10px 28px;
    box-shadow: 0 2px 8px rgba(29,158,117,0.25);
    transition: all 0.2s ease;
}
div.stButton > button:hover {
    background-color: #1D9E75;
    color: white;
    box-shadow: 0 4px 14px rgba(29,158,117,0.4);
}
</style>
""", unsafe_allow_html=True)


st.title('Customer Segmentation Analysis 🎯')
st.write('Enter Customer Details to Predict Segment:')

col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider('Age', min_value=18, max_value=100, value=30)
    Income = st.slider('Income', min_value=0, max_value=200000, value=40000)
    Total_Spending = st.slider('Total Spendings (Sum of Purchases)', min_value=0, max_value=10000, value=1000)


with col2:
    Number_Store_Purchases = st.number_input('Number of Store Purchases', min_value=0, max_value=50, value=10)
    Number_Web_Purchases = st.number_input('Number of Web Purchases', min_value=0, max_value=70, value=15)
    Number_Web_Visits_Month = st.number_input('Number of Website Visits per Month', min_value=0, max_value=30, value=10)
    Response = st.number_input('Response (Days since last purchase)', min_value=0, max_value=365, value=24)


if st.button("Predict Segment"):
    input_data = pd.DataFrame({
     'Age': [age],
     'Income': [Income],
     'total_spendings': [Total_Spending],
     'NumStorePurchases': [Number_Store_Purchases],
     'NumWebPurchases': [Number_Web_Purchases],
     'NumWebVisitsMonth': [Number_Web_Visits_Month],
     'Response': [Response]
    })

    input_scaled = scaler.transform(input_data)

# if st.button('Predict Segment'):
#
#     clusters = kmeans.predict(input_scaled)[0]
#
#     st.success(f"Predicted Segment: Cluster {clusters}")


# if st.button('Predict Segment'):
    cluster_id = kmeans.predict(input_scaled)[0]
    seg        = SEGMENT_INFO[cluster_id]
    means      = CLUSTER_MEANS[cluster_id]

    with col3:    # --- Result header ---
        st.markdown(f"""
            <div style="
                background-color:{seg['color']}18;
                border-left:4px solid {seg['color']};
                border-radius:8px;
                padding:16px 20px;
                margin:16px 0 8px 0;">
                <div style="font-size:12px;color:#888;margin-bottom:4px;">Predicted segment</div>
                <div style="font-size:20px;font-weight:700;color:{seg['color']};">
                    Cluster {cluster_id} — {seg['name']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # --- Fix issue 1: grouped bar chart, no overlapping ---
        customer_vals = [
            age, Income, Total_Spending,
            Number_Store_Purchases, Number_Web_Purchases,
            Number_Web_Visits_Month, Response
        ]

        labels = [f["label"] for f in FEATURE_CONFIG]
        colors = [f["color"] for f in FEATURE_CONFIG]
        maxvals = [f["max"] for f in FEATURE_CONFIG]
        keys = [f["key"] for f in FEATURE_CONFIG]
        fmts = [f["fmt"] for f in FEATURE_CONFIG]

        cust_pct = [round(min(v / m, 1.0) * 100) for v, m in zip(customer_vals, maxvals)]
        avg_pct = [round(min(means[k] / m, 1.0) * 100) for k, m in zip(keys, maxvals)]

        # Fix issue 2: text labels placed cleanly outside bars, no overlap
        cust_text = [fmt(v) for fmt, v in zip(fmts, customer_vals)]
        avg_text = [fmt(means[k]) for fmt, k in zip(fmts, keys)]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name="Cluster average",
            y=labels,
            x=avg_pct,
            orientation="h",
            marker_color="rgba(180,180,180,0.4)",
            marker_line_color="rgba(150,150,150,0.7)",
            marker_line_width=1,
            text=avg_text,
            textposition="outside",
            textfont=dict(size=11, color="#888888"),
            cliponaxis=False,
            width=0.35,
        ))

        fig.add_trace(go.Bar(
            name="This customer",
            y=labels,
            x=cust_pct,
            orientation="h",
            marker_color=colors,
            marker_opacity=0.9,
            text=cust_text,
            textposition="outside",
            textfont=dict(size=11),
            cliponaxis=False,
            width=0.35,
        ))

        fig.update_layout(
            barmode="group",
            bargap=0.25,
            bargroupgap=0.08,
            # title=dict(text="Customer vs cluster average", x=0, font=dict(size=12)),
            xaxis=dict(range=[0, 145], showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, autorange="reversed", tickfont=dict(size=12)),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=90, t=40, b=10),
            height=360,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="left", x=0, font=dict(size=11)
            ),
        )

        st.plotly_chart(fig, use_container_width=True)