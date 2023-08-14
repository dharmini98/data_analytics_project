#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install confluent-kafka')
get_ipython().system('pip install kafka-python')
get_ipython().system('pip install fbprophet')
get_ipython().system('pip install yfinance ')


# In[ ]:


from kafka import KafkaProducer, KafkaConsumer
import warnings
from kafka import KafkaProducer
import json
import yfinance as yf
import time
from kafka import KafkaConsumer
import json



# Verify Kafka broker connection using a KafkaProducer
def verify_kafka_producer_connection():
    try:
        producer = KafkaProducer(bootstrap_servers='localhost:9092') #change boostrap_servers to cloud if needed
        print("Kafka Producer connected successfully.")
    except Exception as e:
        print(f"Error connecting to Kafka Producer: {e}")

# Verify Kafka broker connection using a KafkaConsumer
def verify_kafka_consumer_connection():
    try:
        consumer = KafkaConsumer('test_topic', bootstrap_servers='localhost:9092')
        print("Kafka Consumer connected successfully.")
    except Exception as e:
        print(f"Error connecting to Kafka Consumer: {e}")

if __name__ == "__main__":
    verify_kafka_producer_connection()
    verify_kafka_consumer_connection()


# In[ ]:


def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    stock_data = stock.history(period='1d')
    return stock_data.to_dict('records')

def run_kafka_producer():
    producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    topic = 'stock_data_topic'
    symbol = 'TSLA'
    #symbol = ['AAPL', 'GOOG', 'TSLA']  # Replace this with the stock symbol you want to fetch data for

    while True:
        stock_data = fetch_stock_data(symbol)
        producer.send(topic, value=stock_data)
        print(f"{stock_data}")
        time.sleep(1)
'''       
def process_stock_data(stock_data):
    # Implement your code here to process and analyze stock data
    print(f"Received: {stock_data}")

def run_kafka_consumer():
    consumer = KafkaConsumer('stock_data_topic', bootstrap_servers='localhost:9092', value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    for message in consumer:
        stock_data = message.value
        process_stock_data(stock_data)
        
        
        '''
if __name__ == "__main__":
    run_kafka_producer()
    run_kafka_consumer()

