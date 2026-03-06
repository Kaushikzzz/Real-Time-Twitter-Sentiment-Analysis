# Real-Time Twitter Sentiment Analysis Pipeline

## Overview

This project implements a real-time data pipeline to analyze sentiment from streaming tweet-like text data. The system ingests high-velocity data, processes it using a distributed streaming framework, stores the results in a database, and visualizes sentiment trends through a live dashboard.

The objective of this project is to demonstrate how modern data engineering tools can be combined to process and analyze streaming data in near real time.

## Tech Stack

* **Programming Language:** Python
* **Streaming Platform:** Apache Kafka, Zookeeper
* **Processing Engine:** Apache Spark (PySpark 3.2.4)
* **Database:** MongoDB (NoSQL)
* **Visualization:** Streamlit, Altair
* **NLP Library:** VADER Sentiment Analysis

## System Architecture

**1. Data Ingestion**
A Python-based producer simulates live tweet streams and continuously publishes messages to an Apache Kafka topic.

**2. Stream Processing**
Apache Spark Structured Streaming consumes the Kafka stream and performs real-time sentiment classification using the VADER sentiment lexicon. Each tweet is categorized as **Positive**, **Negative**, or **Neutral**.

**3. Data Storage**
The processed results are written to a MongoDB collection, enabling efficient storage and fast retrieval for analytics.

**4. Data Visualization**
A Streamlit dashboard queries MongoDB at regular intervals (every ~2 seconds) to display:

* Live sentiment counts
* Sentiment distribution charts
* Streaming tweet data

## Performance Highlights

* **Low Latency:** End-to-end processing latency is typically under ~2 seconds for each micro-batch.
* **Scalable Design:** Kafka and Spark provide a decoupled architecture that can scale horizontally with increasing data volume.
* **Fault Tolerance:** Spark streaming checkpointing ensures recovery and reliability during failures.

## Installation and Usage

1. Start **Zookeeper** and **Apache Kafka** services.
2. Ensure **MongoDB** is running on the default port (`27017`).
3. Install project dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Kafka producer:

```bash
python producer.py
```

5. Start the Spark streaming job:

```bash
python spark_stream.py
```

6. Launch the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

Once the pipeline is running, the dashboard will automatically update as new data flows through the system.
