# ChainSight AI - Inventory Dashboard

**Smarter Supply Chain Insights for Small Businesses**

ChainSight AI is an intelligent inventory analytics app built with Streamlit. It helps small and mid-sized businesses manage their inventory smarter by offering instant insights, out-of-stock alerts, category summaries, and visualizations — all from a simple CSV file upload.

## Features

- Upload your inventory CSV file and instantly get:
  - **Total Inventory Value**
  - **Out-of-Stock Item Alerts**
  - **Reorder Suggestions (Low Stock)**
  - **Category-Level Summaries**
  - **Interactive Visualizations (Stock Distribution)**
  - **Data Quality Checks**
- Option to **Download Processed Data**
- Designed to be simple, smart, and recruiter-friendly
- Future-ready: AI-based inventory forecasting (coming soon!)

## How to Use

1. Go to the app: [ChainSight AI Dashboard](https://chainsight-ai.streamlit.app)
2. Upload your inventory `.csv` file
3. Explore the insights generated automatically
4. Download the processed file if needed

## Sample CSV Format

Your CSV file should have the following **minimum columns**:

| Product_Name | Available_Stock | Unit_Cost | Category (optional) |
|--------------|------------------|-----------|----------------------|
| Widget A     | 120              | 5.50      | Tools                |
| Widget B     | 0                | 3.25      | Tools                |
| Widget C     | 45               | 7.00      | Hardware             |

**Required Columns:**
- `Available_Stock`
- `Unit_Cost`

**Optional Columns:**
- `Product_Name`, `Category` — used for better reporting and summaries

> **Note:** Column names should be exactly as shown (case-sensitive and no leading/trailing spaces).

## Tech Stack

- Python
- Streamlit
- Pandas
- Matplotlib + Seaborn

## Upcoming Features

- AI-powered demand forecasting
- Sales trends and reorder predictions
- Email alerts for low-stock items
- User authentication and cloud storage

---

## Run Locally

1. Clone the repository:
```bash
git clone https://github.com/sairam66/ChainSight-AI.git
cd ChainSight-AI
