#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install confluent-kafka')
get_ipython().system('pip install kafka-python')
get_ipython().system('pip install fbprophet')
get_ipython().system('pip install yfinance ')
get_ipython().system('pip install mysql')
get_ipython().system('pip install mysql-connector-python')


# In[ ]:

#check github update
from kafka import KafkaProducer, KafkaConsumer
import json
import yfinance as yf
import threading
import pandas as pd
import time
from datetime import datetime
import plotly.express as px
import mysql.connector

# In[ ]:

def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    stock_data = stock.history(period='1d')
    return stock_data.to_dict('records')


# Process and analyze stock data in real-time
def process_stock_data(stock_data):
    df = pd.DataFrame(stock_data)
    current_time = pd.Timestamp.now()
    df['timestamp'] = current_time
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.rename(columns={'Date': 'timestamp', 'Close': 'closing_price', 'Stock Splits': 'Stock_Splits' })

    '''
    # Calculate percentage change and rolling average
    df['timestamp'] = pd.to_datetime(df['timestamp']) #changes to pandas datetime object
    df.set_index('timestamp', inplace=True)           #sets timestamp as index to dataframe
    df['percentage_change'] = df['closing_price'].pct_change() * 100  #computes percentage change from immediate prev row
    df['rolling_average'] = df['closing_price'].rolling(window=5).mean() #

    # Anomaly detection: Identify significant percentage changes
    threshold = 2  # Define the anomaly threshold (adjust as needed)
    df['anomaly'] = df['percentage_change'].abs() > threshold

    # Plot real-time analysis using Plotly
    fig = px.line(df, x=df.index, y=['closing_price', 'rolling_average'], title='Real-Time Stock Analysis')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Price')

    anomaly_trace = px.scatter(df[df['anomaly']], x=df.index, y='closing_price', color_discrete_sequence=['red'],
                               title='Anomalies', labels={'closing_price': 'Closing Price'})
    fig.add_trace(anomaly_trace.data[0]) #?

    percentage_change_fig = px.bar(df, x=df.index, y='percentage_change', color='anomaly', title='Percentage Change and Anomalies',
                                    labels={'percentage_change': 'Percentage Change'})
    percentage_change_fig.update_xaxes(title_text='Date')
    percentage_change_fig.update_yaxes(title_text='Percentage Change')

    fig.update_layout(updatemenus=[{'buttons': [{'method': 'relayout', 'label': 'Percentage Change',
                                                  'args': [{'yaxis.title.text': 'Percentage Change',
                                                            'yaxis2.title.text': 'Percentage Change'}]},
                                                 {'method': 'relayout', 'label': 'Price',
                                                  'args': [{'yaxis.title.text': 'Price',
                                                            'yaxis2.title.text': 'Price'}]}]}],
                         showlegend=True)

    fig.show()
    '''
    # Insert data into MySQL
    insert_into_mysql(df)

def run_kafka_producer():
    producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    topic = 'stock_data_topic'
    symbol = 'AAPL'
    #symbol = ['AAPL', 'GOOG', 'TSLA']  # Replace this with the stock symbol you want to fetch data for

    while True:
        stock_data = fetch_stock_data(symbol)
        producer.send(topic, value=stock_data)
        print(f"Published:{stock_data}")
        time.sleep(5)


def run_kafka_consumer():
    consumer = KafkaConsumer('stock_data_topic', bootstrap_servers='localhost:9092', value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    for message in consumer:
        stock_data = message.value
        process_stock_data(stock_data)
        
# Insert data into MySQL
def insert_into_mysql(data):
    db_config = {
        "host": "localhost",
        "user": "root",      # Replace with your MySQL username
        "password": "ni$ha17111998",  # Replace with your MySQL password
        "database": "stock"
    }

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 

    create_table_query = """
    CREATE TABLE IF NOT EXISTS stock_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME ,
        Open DECIMAL(18, 2),
        High DECIMAL(18, 2),
        Low DECIMAL(18, 2),
        closing_price DECIMAL(18, 2),
        volume BIGINT,
        Dividends DECIMAL(18, 2),
        Stock_Splits DECIMAL(18, 2)
    )
    """
    cursor.execute(create_table_query)

    conn.commit()
    #conn.close()       

    table_name = 'stock_data'
    data_frame_name = data

    #data = df
    data_dict_list = data.to_dict(orient='records')
    #return data_dict_list
    #values = data.to_records(index=False)
    values = data_dict_list
    
    table_name = 'stock_data'

    columns = ', '.join(values[0].keys())
    placeholders = ', '.join(['%s'] * len(values[0]))

    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    insert_values = [(value['Open'], value['High'], value['Low'], value['closing_price'],
                  value['Volume'], value['Dividends'], value['Stock_Splits'], value['timestamp']) for value in values]

    cursor.executemany(insert_query, insert_values)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Create and start the Kafka producer in a separate thread
    producer_thread = threading.Thread(target=run_kafka_producer)
    producer_thread.start()

    # Run the Kafka consumer in the main thread
    run_kafka_consumer()

