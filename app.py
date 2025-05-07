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


                if forecast_file is not None:
                    try:
                        df = pd.read_csv(forecast_file)
                        df.columns = df.columns.str.strip()
                        df['Date'] = pd.to_datetime(df['Date'])
                        df.set_index('Date', inplace=True)
                        df = df.asfreq('D').fillna(method='ffill')  # daily frequency

                        st.subheader("Uploaded Sales Data")
                        st.line_chart(df['Units_Sold'])

                        model = SARIMAX(df['Units_Sold'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))
                        results = model.fit(disp=False)

                        forecast_steps = 15
                        forecast = results.forecast(steps=forecast_steps)

                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=df.index, y=df['Units_Sold'], name="Actual"))
                        future_dates = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=forecast_steps)
                        fig.add_trace(go.Scatter(x=future_dates, y=forecast, name="Forecast"))
                        st.plotly_chart(fig, use_container_width=True)

                        st.metric("Forecasted Total Units (Next 15 Days)", int(forecast.sum()))
