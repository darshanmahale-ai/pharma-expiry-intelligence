import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Pharma Expiry Intelligence", layout="wide")

st.title("💊 AI Expiry Intelligence Add-On for Care / Marg")
st.caption("Built by Darshan Mahale | B.Pharm + AI Consultant Pune")

uploaded = st.file_uploader("Upload your Care/Marg Excel", type=["xlsx","csv"])

if uploaded is None:
    st.info("Upload your file to see AI Report. Sample columns needed: Product, Expiry_Date, Stock_Left, Quantity_Sold, Sales_Amount")
    st.stop()

# Load file
if uploaded.name.endswith('csv'):
    df = pd.read_csv(uploaded)
else:
    df = pd.read_excel(uploaded)

# Convert dates safely
df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date'], errors='coerce')
df['Expiry_Days'] = (df['Expiry_Date'] - datetime.now()).dt.days
df['Sales_Velocity'] = df['Quantity_Sold'] / 180

def get_status(row):
    if row['Expiry_Days'] < 30 and row['Stock_Left'] > row['Sales_Velocity'] * 30:
        return "RED - Confirm Loss"
    elif row['Expiry_Days'] < 60:
        return "YELLOW - Push Urgently"
    else:
        return "GREEN - Will Sell"

df['AI_Action'] = df.apply(get_status, axis=1)

# KPIs
col1, col2, col3 = st.columns(3)
red_df = df[df['AI_Action'].str.contains('RED')]
yellow_df = df[df['AI_Action'].str.contains('YELLOW')]

col1.metric("Confirm Loss Value", f"Rs {red_df['Sales_Amount'].sum():,.0f}")
col2.metric("Push Urgently", len(yellow_df))
col3.metric("Safe Stock", len(df) - len(red_df) - len(yellow_df))

st.subheader("🔴 RED - Return to Distributor NOW")
st.dataframe(red_df)

st.subheader("🟡 YELLOW - Push via Doctor/MR")
st.dataframe(yellow_df)

# FIXED DOWNLOAD BUTTON
csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Action Report",
    data=csv_data,
    file_name="expiry_action_report.csv",
    mime="text/csv"
)
