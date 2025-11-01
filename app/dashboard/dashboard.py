
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Title
st.set_page_config(page_title="Geo-Enrichment Dashboard", layout="wide")
st.title("Geo-Enrichment Dashboard")

# DataBase Connection
@st.cache_data
def load_data():
    conn = sqlite3.connect("geo_data.db")
    df = pd.read_sql_query("SELECT * FROM enriched_location", conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("No enriched locations found")
else:
    st.subheader(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.dataframe(df)

    # Map visualization
    st.subheader("Location")
    st.map(df.rename(columns={"latitude":"lat", "longitude":"lon"}))

    # Stat
    st.subheader("Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Temperature (C)", round(df['temperature'].mean(), 2))
    with col2:
        st.metric("Avg wind speed (km/h)", round(df['windspeed'].mean(), 2))
