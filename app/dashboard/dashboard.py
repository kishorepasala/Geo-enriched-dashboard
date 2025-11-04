import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import requests


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


API_URL = "http://127.0.0.1:8000"

st.title("Geo-Enrichment Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your address CSV", type=["csv"])

if uploaded_file is not None:
    with st.spinner("Uploading and processing..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{API_URL}/upload", files={"file": (uploaded_file.name, uploaded_file.getvalue())})

        if response.status_code == 200:
            st.success("✅ File uploaded successfully!")
            st.json(response.json())
        else:
            st.error(f"❌ Upload failed: {response.text}")


def load_data():
    conn = sqlite3.connect("geo_data.db")
    df = pd.read_sql_query("SELECT * FROM enriched_location", conn)
    conn.close()
    return df

if st.button("View Enriched Data"):
    try:
        df = load_data()
        st.dataframe(df)
    except Exception as e:
        st.error("Failed to load data: {e}")
