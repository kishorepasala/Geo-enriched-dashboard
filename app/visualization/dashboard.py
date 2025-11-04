import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

DB_PATH = "geo_data.db"

st.set_page_config(page_title="Geo-Enrichment Dashboard", layout="wide")

st.title("🌍 Geo-Enrichment Dashboard")
st.markdown("Visualize weather, air quality, and location data from the pipeline.")

# Load data
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM enriched_location", conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("No data found in the database. Run the pipeline first.")
else:
    st.success(f"Loaded {len(df)} enriched records")

    # Map visualization
    st.subheader("📍 Locations Map")
    st.map(df, latitude="latitude", longitude="longitude")

    # Weather overview
    st.subheader("🌡️ Weather Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Temperature (°C)", f"{df['temperature'].mean():.2f}")
    col2.metric("Avg Humidity (%)", f"{df['humidity'].mean():.2f}")
    col3.metric("Avg Wind Speed (m/s)", f"{df['wind_speed'].mean():.2f}")

    # Air quality graph
    st.subheader("💨 Air Quality Overview")
    fig = px.scatter(
        df,
        x="pm2_5",
        y="aqi",
        color="temperature",
        size="pm10",
        hover_name="address",
        title="AQI vs PM2.5 (color = temperature)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Data table
    st.subheader("📊 Data Table")
    st.dataframe(df)
