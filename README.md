Real-Time Twitter Sentiment Analysis Pipeline
This project implements a real-time data engineering pipeline to process and visualize sentiment trends from streaming text data. It uses a distributed architecture to handle high-velocity data with sub-2-second latency.

Technical Stack

Language: Python 


Streaming: Apache Kafka & Zookeeper 


Processing: Apache Spark (PySpark) 3.2.4 


Database: MongoDB (NoSQL) 


Visualization: Streamlit & Altair 


NLP: VADER Sentiment Analysis 

System Architecture

Data Ingestion: A Python-based producer generates synthetic tweet streams and transmits data to an Apache Kafka topic.


Stream Processing: Spark Structured Streaming consumes the Kafka feed, performing real-time sentiment classification (Positive, Negative, Neutral).


Data Persistence: Processed records are stored in a MongoDB collection for high-write throughput.


Visualization: A Streamlit dashboard queries MongoDB at 2-second intervals to display live KPIs and sentiment distribution.

Key Features

Sub-2-Second Latency: Optimized for real-time micro-batch processing.


Local Compatibility: Configured specifically for Spark 3.2.4 to ensure compatibility with Windows Hadoop utilities.


Fault Tolerance: Utilizes a decoupled architecture for reliable data handling.

Installation and Usage
Start Zookeeper and Apache Kafka services.

Ensure MongoDB is active on the default port (27017).

Install dependencies:


pip install -r requirements.txt 

Run the components:


python producer.py 


python spark_stream.py 


streamlit run dashboard.py
