import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="ChainSight AI - Inventory", layout="wide")
st.title("ChainSight AI - Inventory Dashboard")
st.subheader("Smarter Supply Chain Insights for Small Businesses")

# File uploader
uploaded_file = st.file_uploader("Upload your inventory CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Load and clean data
        data = pd.read_csv(uploaded_file)
        data.columns = data.columns.str.strip()  # Clean column names
        # --- FILTERS ---
st.subheader("🔍 Filter Inventory Data")

# Filter by Category
category_options = ['All'] + sorted(data['Category'].dropna().unique().tolist())
selected_category = st.selectbox("Select Category", category_options)

# Filter by Product
product_options = ['All'] + sorted(data['Product'].dropna().unique().tolist())
selected_product = st.selectbox("Select Product", product_options)

# Apply filters
filtered_data = data.copy()

if selected_category != 'All':
    filtered_data = filtered_data[filtered_data['Category'] == selected_category]

if selected_product != 'All':
    filtered_data = filtered_data[filtered_data['Product'] == selected_product]

# Show filtered data
st.write("### Filtered Inventory Data")
st.dataframe(filtered_data)

        # Show raw data
        st.write("### Inventory Data", data)
        st.write("Detected Columns:", data.columns.tolist())  # For debugging

        # Calculate total inventory value and out-of-stock items
        if 'Available_Stock' in data.columns and 'Unit_Cost' in data.columns:
            data['Total_Value'] = data['Available_Stock'] * data['Unit_Cost']
            total_inventory_value = data['Total_Value'].sum()

            out_of_stock_items = data[data['Available_Stock'] == 0]
            out_of_stock_count = out_of_stock_items.shape[0]

            # KPI Metrics
            col1, col2 = st.columns(2)
            col1.metric("Total Inventory Value", f"${total_inventory_value:,.2f}")
            col2.metric("Out-of-Stock Items", out_of_stock_count)

            # Show out-of-stock items
            if out_of_stock_count > 0:
                st.subheader("⚠️ Out-of-Stock Products")
                st.dataframe(out_of_stock_items)

        else:
            st.warning("CSV must contain 'Available_Stock' and 'Unit_Cost' columns.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

else:
    st.info("Please upload a CSV file to begin.")
