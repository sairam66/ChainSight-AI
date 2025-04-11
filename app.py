import streamlit as st
import pandas as pd

# --- UI HEADER ---
st.set_page_config(page_title="ChainSight AI", page_icon=":package:", layout="wide")

st.title("ChainSight AI")
st.subheader("Smarter Supply Chain Visibility for SMEs")

st.markdown("""
Welcome to **ChainSight AI**, your intelligent supply chain dashboard that helps small and mid-sized businesses get real-time insights into their inventory performance, demand trends, and supplier health.  
""")

st.divider()
# Load your inventory CSV
data = pd.read_csv('./data/inventory_data.csv')

# --- KPI METRICS ---
total_skus = data['Item'].nunique()
# Calculate Total Inventory Value using correct column names from your CSV
if 'Available Stock' in data.columns and 'Unit Cost' in data.columns:
    data['Total_Value'] = data['Available Stock'] * data['Unit Cost']
    inventory_value = data['Total_Value'].sum()
    st.metric("Total Inventory Value", f"${inventory_value:,.2f}")
else:
    st.warning("Skipping total value calculation. 'Available Stock' or 'Unit Cost' column not found.")
inventory_value = total_value.sum()
out_of_stock = data[data['Stock Quantity'] == 0].shape[0]

# --- Show metrics in columns ---
col1, col2, col3 = st.columns(3)

col1.metric("Total Unique SKUs", total_skus)
col2.metric("Total Inventory Value", f"${inventory_value:,.2f}")
col3.metric("Out-of-Stock Items", out_of_stock)

st.divider()

# Show full inventory
st.subheader("📦 Current Inventory Levels")
st.dataframe(data)

# Low Stock Alert
low_stock = data[data['Current_Stock'] < data['Reorder_Level']]
st.subheader("⚠️ Items Below Reorder Level")
st.table(low_stock)

# Supplier Delay Alert
delayed_suppliers = data[data['Days_Since_Last_Delivery'] > 10]
st.subheader("🚨 Suppliers With Delays")
st.table(delayed_suppliers)
