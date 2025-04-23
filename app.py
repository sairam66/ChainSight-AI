import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings

warnings.filterwarnings("ignore")


# --- App Config & Heading ---
st.set_page_config(page_title="ChainSight AI", layout="wide")
st.title("ChainSight AI")
st.subheader("Smarter Inventory Analytics for Small & Mid-sized Businesses")

st.markdown("""
Welcome to **ChainSight AI**, a lightweight yet powerful inventory analytics tool.  
Just upload your `.csv` file and get real-time visibility into stock levels, inventory value, and out-of-stock products.

#### **CSV Format Required**:
Ensure your CSV file includes the following columns:
- `Product`
- `Category`
- `Available_Stock`
- `Unit_Cost`
""")

st.divider()

# Upload Inventory File
uploaded_file = st.file_uploader("Upload your inventory CSV file", type="csv")


# CSV Conversion Helper
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


# Main Logic
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        data.columns = data.columns.str.strip()
        st.write("### Inventory Data")
        st.dataframe(data)

        if 'Available_Stock' in data.columns and 'Unit_Cost' in data.columns:

            data['Total_Value'] = data['Available_Stock'] * data['Unit_Cost']
            total_inventory_value = data['Total_Value'].sum()
            out_of_stock_items = data[data['Available_Stock'] == 0]

            col1, col2 = st.columns(2)
            col1.metric("Total Inventory Value", f"${total_inventory_value:,.2f}")
            col2.metric("Out-of-Stock Items", out_of_stock_items.shape[0])


            csv = convert_df(data)
            st.download_button("Download Processed Data", csv, "processed_inventory.csv", "text/csv")

            if not out_of_stock_items.empty:

                st.subheader("⚠️ Out-of-Stock Products")
                st.dataframe(out_of_stock_items)

            st.subheader("Reorder Suggestions (Stock < 10)")
            low_stock = data[data['Available_Stock'] < 10]
            st.dataframe(low_stock if not low_stock.empty else pd.DataFrame(
                {"Message": ["All items have healthy stock levels."]}))


            st.subheader("Stock Level Distribution")
            fig, ax = plt.subplots()
            sns.histplot(data['Available_Stock'], bins=20, kde=True, ax=ax)
            ax.set_xlabel("Stock")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

            if 'Category' in data.columns:
                st.subheader("Category-Level Inventory Summary")
                summary = data.groupby('Category').agg({
                    'Available_Stock': 'sum',
                    'Total_Value': 'sum'
                }).sort_values('Total_Value', ascending=False)
                st.dataframe(summary)

                # Forecasting Module (SARIMAX)
                st.header("📈 Demand Forecasting (SARIMAX)")
                forecast_file = st.file_uploader("Upload Sales CSV (Date, Units_Sold)", type="csv", key="forecast")


                # Data upload and filtering section (existing code)
st.title("Inventory Management System")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())  # Show the first few rows of the data

    # Process and filter data as needed (e.g., converting 'Date' to datetime, cleaning NaN values)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df = df.sort_values('Date')

    # ----------------------------- Forecasting Section -----------------------------
    st.markdown("## 📈 Demand Forecasting")
    st.info("""
    This section uses **SARIMAX** to forecast the next 6 months of inventory levels based on historical data.

    ### How to Use:
    - Make sure your uploaded file has at least 12 months of data.
    - Required columns:
      - `Date`: Must be in YYYY-MM-DD format
      - `Product`: Product name or ID
      - `Available_Stock`: Inventory level on that date
    - Select a product from the dropdown to generate the forecast.

    **Note:** If your data doesn’t have enough history (12+ months), the forecast won’t run.
    """)

    # Offer sample forecast template download
    sample_data = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=15, freq='M'),
        "Product": ["Product A"] * 15,
        "Available_Stock": [100, 120, 110, 130, 125, 140, 135, 150, 160, 170, 180, 190, 200, 210, 220]
    })
    sample_csv = sample_data.to_csv(index=False).encode('utf-8')
    st.download_button("📄 Download Sample Forecast Template", sample_csv, "sample_forecast_template.csv", "text/csv")

    # Forecasting logic
    try:
        if 'Date' in df.columns and 'Product' in df.columns and 'Available_Stock' in df.columns:
            product_list = df['Product'].dropna().unique()
            selected_product = st.selectbox("Select a product to forecast", product_list)

            product_data = df[df['Product'] == selected_product].copy()
            product_data['Date'] = pd.to_datetime(product_data['Date'], errors='coerce')
            product_data.dropna(subset=['Date'], inplace=True)
            product_data.set_index('Date', inplace=True)

            # Group and resample by month
            monthly_data = product_data['Available_Stock'].resample('M').sum()

            if len(monthly_data) >= 12:
                from statsmodels.tsa.statespace.sarimax import SARIMAX
                import plotly.graph_objects as go

                model = SARIMAX(monthly_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
                results = model.fit(disp=False)

                forecast = results.get_forecast(steps=6)
                forecast_df = forecast.conf_int()
                forecast_df['Forecast'] = forecast.predicted_mean
                forecast_df.index = pd.date_range(start=monthly_data.index[-1] + pd.DateOffset(months=1), periods=6, freq='M')

                # Plotting
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data, name='Historical'))
                fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['Forecast'], name='Forecast'))
                fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['upper Available_Stock'], name='Upper CI', line=dict(dash='dash')))
                fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['lower Available_Stock'], name='Lower CI', line=dict(dash='dash')))
                fig.update_layout(title="6-Month Inventory Forecast", xaxis_title="Date", yaxis_title="Available Stock")
                st.plotly_chart(fig)

                # Export forecast as CSV
                csv = forecast_df.to_csv().encode('utf-8')
                st.download_button("📥 Download Forecast CSV", data=csv, file_name='forecast.csv', mime='text/csv')
            else:
                st.warning("Not enough monthly data to forecast. Please upload at least 12 months of data.")
        else:
            st.warning("Dataset must contain 'Date', 'Product', and 'Available_Stock' columns.")
    except Exception as e:
        st.error(f"Error while generating forecast: {e}")
