import streamlit as st
import pandas as pd
import numpy as np
import joblib

kmeans=joblib.load('kmeans_model.pkl')
scaler=joblib.load('scaler.pkl')

st.title('Customer Segmentation App')
st.write('Enter Customer Details to Predict Segment:')

age = st.number_input('Age', min_value=18, max_value=100, value=30)
Income = st.number_input('Income', min_value=0, max_value=200000, value=40000)
Total_Spending = st.number_input('Total Spendings (Sum of Purchases)', min_value=0, max_value=10000, value=1000)
Number_Store_Purchases = st.number_input('Number of Store Purchases',min_value=0, max_value=1000, value=10)
Number_Web_Purchases =st.number_input('Number of Web Purchases',min_value=0, max_value=200, value=15)
Number_Web_Visits_Month = st.number_input('Number of Website Visits per Month',min_value=0, max_value=800, value=180)
Response = st.number_input('Response (Days since last purchase)',min_value=0, max_value=365, value=24)

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

if st.button('Predict Segment'): 

    clusters = kmeans.predict(input_scaled)[0]

    st.success(f"Predicted Segment: Cluster {clusters}")