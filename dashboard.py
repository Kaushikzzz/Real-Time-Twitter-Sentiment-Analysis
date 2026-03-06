# Project: Real-Time Twitter Sentiment Analysis
# Module: Streamlit Dashboard
# Feature: Auto-refresh every 2 seconds, Live Charts, Raw Data Feed.

import streamlit as st
import pandas as pd
from pymongo import MongoClient
import time
import altair as alt

st.set_page_config(
    page_title="Twitter Sentiment Live",
    page_icon="Twitter",
    layout="wide",
)

st.title("Real-Time Twitter Sentiment Analysis")
st.markdown("Live Data from Kafka & Spark Streaming")

@st.cache_resource
def init_connection():
    return MongoClient("mongodb://localhost:27017/")

client = init_connection()
db = client["twitter_project"]
collection = db["tweets"]

placeholder = st.empty()

while True:

    data = list(collection.find().sort("_id", -1).limit(100))
    
    with placeholder.container():

        if data:
            df = pd.DataFrame(data)


            total_count = collection.count_documents({})
            pos_count = len(df[df['sentiment'] == 'Positive'])
            neg_count = len(df[df['sentiment'] == 'Negative'])
            neu_count = len(df[df['sentiment'] == 'Neutral'])

            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("Total Tweets Processed", total_count)
            kpi2.metric("Positive (+ve)", pos_count, delta="Good Vibes")
            kpi3.metric("Negative (-ve)", neg_count, delta="-Bad Vibes", delta_color="inverse")
            kpi4.metric("Neutral (0)", neu_count)

            st.divider()


            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("Live Sentiment Trends")
                chart_data = pd.DataFrame({
                    'Sentiment': ['Positive', 'Negative', 'Neutral'],
                    'Count': [pos_count, neg_count, neu_count]
                })
                
                chart = alt.Chart(chart_data).mark_bar().encode(
                    x='Sentiment',
                    y='Count',
                    color=alt.Color('Sentiment', scale=alt.Scale(domain=['Positive', 'Negative', 'Neutral'], range=['green', 'red', 'gray'])),
                    tooltip=['Sentiment', 'Count']
                ).properties(height=400)
                
                st.altair_chart(chart, use_container_width=True)

            with col2:
                st.subheader("Latest Tweets Feed")
                st.dataframe(df[['text', 'sentiment']].head(10), hide_index=True, use_container_width=True)
        
        else:
            st.warning("Waiting for data from Spark...")


    time.sleep(2)