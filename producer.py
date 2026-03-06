# Project: Real-Time Twitter Sentiment Analysis
# Module: Data Producer (Fake Simulation)
# Author: Kaushik Prakash and team
# Note: Using fake simulation as Twitter's API is paid now with 100$/Month!

import time
import json
import random
from kafka import KafkaProducer

TOPIC_NAME = "twitter"
BOOTSTRAP_SERVERS = 'localhost:9092'

KEYWORDS = ["Modi", "Rahul", "Cricket", "AI", "Economy", "Movie", "Tech"]
POSITIVE_TEXTS = ["is amazing!", "victory for India", "great performance", "love this", "superb logic", "growing fast"]
NEGATIVE_TEXTS = ["is a disaster", "failed completely", "worst decision", "disappointed", "crisis ahead", "waste of time"]
NEUTRAL_TEXTS = ["is happening today", "discussed in parliament", "match updates", "launched new features", "press conference at 5 PM"]

def generate_tweet():
    topic = random.choice(KEYWORDS)
    sentiment_type = random.choice(["pos", "neg", "neu"])
    
    if sentiment_type == "pos":
        text = f"{topic} {random.choice(POSITIVE_TEXTS)}"
    elif sentiment_type == "neg":
        text = f"{topic} {random.choice(NEGATIVE_TEXTS)}"
    else:
        text = f"{topic} {random.choice(NEUTRAL_TEXTS)}"

    return {
        "id": str(random.randint(100000, 999999)),
        "text": text,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "user": f"User_{random.randint(1, 100)}",
        "location": random.choice(["Delhi", "Mumbai", "Patna", "Bangalore", "Unknown"])
    }

if __name__ == "__main__":
    print("Kafka Producer Startnig.......")
    print(f"Sending Fake Tweet to topic: '{TOPIC_NAME}'")
    
    try:
        producer = KafkaProducer(
            bootstrap_servers=[BOOTSTRAP_SERVERS],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Connected to Kafka succesfuly")
        
        while True:
            tweet = generate_tweet()
            producer.send(TOPIC_NAME, tweet)
            print(f"Sent: {tweet['text']}")
            time.sleep(2)  

    except Exception as e:
        print(f"Unexpected error occured........: {e}")