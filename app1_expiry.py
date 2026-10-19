import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Pharma Expiry Intelligence | Darshan Mahale")

st.title("💊 AI Expiry Intelligence Add-On for Care / Marg")
st.write("Built by Darshan Mahale | B.Pharm + AI Consultant Pune")

uploaded = st.file_uploader("Upload your Care/Marg Excel", type=["xlsx","csv"])

if uploaded:
    df = pd.read_csv(uploaded) if uploaded.name.endswith('csv') else pd.read_excel(uploaded)
    
    # DAX logic in Python
    df['Expiry_Days'] = (pd.to_datetime(df['Expiry_Date']) - datetime.now()).dt.days
    df['Sales_Velocity'] = df['Quantity_Sold'] / 180 # 6 months
    
    def get_status(row):
        if row['Expiry_Days'] < 30 and row['Sales_Velocity'] < row['Stock_Left']/30:
            return "🔴 RED - Confirm Loss - Return Now"
        elif row['Expiry_Days'] < 60 and row['Sales_Velocity'] < 2:
            return "🟡 YELLOW - Push via Doctor"
        else:
            return "🟢 GREEN - Will Sell"

    df['AI_Action'] = df.apply(get_status, axis=1)
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Confirm Loss Value", f"₹ {df[df['AI_Action'].str.contains('RED')]['Sales_Amount'].sum():,}")
    col2.metric("Push Urgently", len(df[df['AI_Action'].str.contains('YELLOW')]))
    col3.metric("Safe Stock", len(df[df['AI_Action'].str.contains('GREEN')]))

    st.dataframe(df[df['AI_Action'].str.contains('RED')])
    
    st.download_button("Download Action Report for Distributor", df.to_csv(), "expiry_action_rep
    
ort.csv")
