import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="ChainSight AI - Inventory", layout="wide")
st.title("ChainSight AI - Inventory Dashboard")
st.subheader("Smarter Supply Chain Insights for Small Businesses")

# File uploader
uploaded_file = st.file_uploader("Upload your inventory CSV file", type="csv")

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
