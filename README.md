\# Real-Time Twitter Sentiment Analysis Pipeline



\## Project Overview

In order to ingest, process, and visualize sentiment trends from streaming text data, this project implements a powerful, real-time data engineering pipeline. High-velocity data streams are handled by the system using a distributed architecture, and a web-based dashboard offers real-time analytical insights.



\## Technical Stack

\* Language: Python

\* Stream Processing: Apache Kafka, Zookeeper

\* Processing Engine: Apache Spark (PySpark) 3.2.4

\* Database: MongoDB (NoSQL)

\* Visualization: Streamlit, Altair

\* NLP Library: VADER Sentiment Analysis



\## System Architecture

1\. Data Ingestion: A Python-based producer simulates live tweet streams, transmitting data to an Apache Kafka topic.

2\. Stream Processing: Apache Spark Structured Streaming consumes the Kafka feed, performing real-time sentiment classification (Positive, Negative, Neutral) using the VADER NLP lexicon.

3\. Data Persistence: Processed records are stored in a MongoDB collection to ensure high-write throughput and data persistence.

4\. Data Visualization: A Streamlit dashboard queries MongoDB at 2-second intervals to display live KPIs, sentiment distribution charts, and raw data feeds.



\## Key Performance Metrics

\* Processing Latency: Achieved sub-2-second end-to-end latency for micro-batch processing.

\* Scalability: Designed with a decoupled architecture (Kafka/Spark) to support horizontal scaling.

\* Reliability: Implemented fault-tolerant streaming logic with checkpointing capabilities.



\## Installation and Usage

1\. Initialize Zookeeper and Apache Kafka services.

2\. Ensure MongoDB is active on the default port (27017).

3\. Install required dependencies: pip install -r requirements.txt

4\. Execute the Producer: python producer.py

5\. Execute the Spark Engine: python spark\_stream.py

6\. Launch the Dashboard: streamlit run dashboard.py

