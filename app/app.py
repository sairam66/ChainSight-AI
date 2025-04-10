import streamlit as st
import pandas as pd

# Load your inventory CSV
data = pd.read_csv('../data/inventory_data.csv')

# Title
st.title("ChainSight AI - Inventory Dashboard")

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
