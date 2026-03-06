# Project: Real-Time Twitter Sentiment Analysis
# Module: Spark Streaming Engine
# Note: Spark 3.2.4 used for compatibility with Windows Hadoop utils (winutils.exe and hodoop.dll)
# Logic: Kafka -> Spark -> VADER Sentiment -> MongoDB

import sys
import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient

KAFKA_TOPIC = "twitter"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
SCALA_VERSION = '2.12'
SPARK_VERSION = '3.2.4'
KAFKA_PACKAGE = f"org.apache.spark:spark-sql-kafka-0-10_{SCALA_VERSION}:{SPARK_VERSION}"

def get_sentiment(text):
    try:
        analyzer = SentimentIntensityAnalyzer()
        if text:
            scores = analyzer.polarity_scores(text)
            compound = scores['compound']
            if compound >= 0.05:
                return "Positive"
            elif compound <= -0.05:
                return "Negative"
            else:
                return "Neutral"
        return "Neutral"
    except Exception:
        return "Neutral"

def save_to_mongo(batch_df, batch_id):
    try:
        if batch_df.count() > 0:
            
            data_list = [row.asDict() for row in batch_df.collect()]
            
            client = MongoClient("mongodb://localhost:27017/")
            db = client["twitter_project"]  
            collection = db["tweets"]       
            

            collection.insert_many(data_list)
            print(f"Saved {len(data_list)} tweets to MongoDB. (Batch ID: {batch_id})")
            
            client.close()
    except Exception as e:
        print(f"Error saving to Mongo: {e}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    os.environ['HADOOP_HOME'] = "C:\\hadoop"
    os.environ['PYSPARK_SUBMIT_ARGS'] = f'--packages {KAFKA_PACKAGE} --conf spark.jars.ivy=C:/ivy pyspark-shell'
    
    print("Starting Spark Streaming -> MongoDB...")

    # 1. CREATE SESSION
    spark = SparkSession.builder \
        .appName("TwitterSentimentAnalysis") \
        .config("spark.jars.packages", KAFKA_PACKAGE) \
        .config("spark.jars.ivy", "C:/ivy") \
        .config("spark.sql.shuffle.partitions", "2") \
        .master("local[*]") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # 2. SCHEMA
    schema = StructType([
        StructField("id", StringType()),
        StructField("text", StringType()),
        StructField("created_at", StringType()),
        StructField("user", StringType()),
        StructField("location", StringType())
    ])

    # 3. READ KAFKA
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "latest") \
        .load()

    # 4. PROCESS
    json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
    sentiment_udf = udf(get_sentiment, StringType())
    processed_df = json_df.withColumn("sentiment", sentiment_udf(col("text")))

    # 5. WRITE TO MONGODB (FOREACHBATCH)
    print("Streaming Start.......Saving to DB..........")
    
    query = processed_df.writeStream \
        .foreachBatch(save_to_mongo) \
        .outputMode("append") \
        .start()

    query.awaitTermination()