import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- App Config & Heading ---
st.set_page_config(page_title="ChainSight AI", layout="wide")

st.title("ChainSight AI")
st.subheader("Smarter Inventory Analytics for Small & Mid-sized Businesses")

st.markdown("""
Welcome to **ChainSight AI**, a lightweight yet powerful inventory analytics tool.  
Just upload your `.csv` file and get real-time visibility into stock levels, inventory value, and out-of-stock products.

#### **CSV Format Required**:
Make sure your CSV file includes the following columns:
- `Product`
- `Category`
- `Available_Stock`
- `Unit_Cost`

You can download a sample template [here](https://chainsight-ai.streamlit.app/inventory_data.csv) or create your own using the same headers.
""")

st.divider()

# Upload CSV
uploaded_file = st.file_uploader("Upload your inventory CSV file", type="csv")

# Helper to download processed file
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# Main logic
if uploaded_file is not None:
    try:
        # Load and clean data
        data = pd.read_csv(uploaded_file)
        data.columns = data.columns.str.strip()

        st.write("### Inventory Data")
        st.dataframe(data)

        # Required columns check
        required_cols = ['Available_Stock', 'Unit_Cost']
        if all(col in data.columns for col in required_cols):
            data['Total_Value'] = data['Available_Stock'] * data['Unit_Cost']
            total_inventory_value = data['Total_Value'].sum()
            out_of_stock_items = data[data['Available_Stock'] == 0]
            out_of_stock_count = out_of_stock_items.shape[0]

            # KPIs
            col1, col2 = st.columns(2)
            col1.metric("Total Inventory Value", f"${total_inventory_value:,.2f}")
            col2.metric("Out-of-Stock Items", out_of_stock_count)

            # Download button
            csv = convert_df(data)
            st.download_button("Download Processed Data", csv, "processed_inventory.csv", "text/csv")

            # Out-of-stock display
            if out_of_stock_count > 0:
                st.subheader("⚠️ Out-of-Stock Products")
                st.dataframe(out_of_stock_items)

            # Low stock alerts
            st.subheader("Reorder Suggestions (Stock < 10)")
            threshold = 10
            low_stock = data[data['Available_Stock'] < threshold]
            if not low_stock.empty:
                st.dataframe(low_stock)
            else:
                st.info("All items have healthy stock levels.")

            # Visualizations
            st.subheader("Stock Level Distribution")
            fig, ax = plt.subplots()
            sns.histplot(data['Available_Stock'], bins=20, kde=True, ax=ax)
            ax.set_xlabel("Stock")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

            # Category-level summary (if present)
            if 'Category' in data.columns:
                st.subheader("Category-Level Inventory Summary")
                category_summary = data.groupby('Category').agg({
                    'Available_Stock': 'sum',
                    'Total_Value': 'sum'
                }).sort_values('Total_Value', ascending=False)
                st.dataframe(category_summary)

            # Data quality check
            st.subheader("Data Quality Check")
            if data.isnull().values.any():
                st.warning("Missing values found in the data.")
                st.dataframe(data[data.isnull().any(axis=1)])
            else:
                st.success("No missing values detected.")

            # Forecasting placeholder
            st.sidebar.header("Coming Soon: Predictive Analytics")
            st.sidebar.info("AI will soon help forecast demand and reorder needs based on sales trends.")

        else:
            st.warning("CSV must contain 'Available_Stock' and 'Unit_Cost' columns.")

    except Exception as e:
        st.error(f"Error processing the file: {e}")
else:
    st.info("Please upload a CSV file to begin.")
