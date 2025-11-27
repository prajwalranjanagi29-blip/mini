import streamlit as st
import pandas as pd
import plotly.express as px
import os

CSV_FILE = "mood_logs.csv"

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Mood Dashboard")

if not os.path.exists(CSV_FILE):
    st.info("No mood data available.")
    st.stop()

df = pd.read_csv(CSV_FILE)
df["date_only"] = pd.to_datetime(df["timestamp"]).dt.date

# Mood entries count per day
counts = df.groupby("date_only").size().reset_index(name="count")
fig = px.bar(counts, x="date_only", y="count", labels={"count": "Entries", "date_only": "Date"})
st.plotly_chart(fig, use_container_width=True)

# Most frequent moods
st.subheader("Most Frequent Moods")
freq = df["mood"].value_counts().reset_index()
freq.columns = ["Mood", "Count"]
st.dataframe(freq)
