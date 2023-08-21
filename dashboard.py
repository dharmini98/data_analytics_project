#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install plotly pandas dash sqlalchemy pymysql')


# In[2]:


get_ipython().system('pip install pandas_ta')


# In[3]:


get_ipython().system('pip install plotly')


# In[4]:


from sqlalchemy import create_engine

# Replace with your database credentials and details
db_url = "mysql+pymysql://root:ni$ha17111998@localhost/stock"
engine = create_engine(db_url)


# In[6]:


import dash
import plotly.graph_objects as go
from dash import dcc as dcc
from dash import html as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import sqlalchemy as sa
import time
import datetime as dt
from datetime import datetime, timedelta

# Set up database connection

app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div(style={'backgroundColor': 'black'}, children=[
    html.H1("Real-time Line Plot Dashboard", style={'color': 'white'}),
    #html.H1("Real-time Line Plot Dashboard"),
    
    # Dropdown to select a column for the first graph
    dcc.Dropdown(
        id='column-dropdown-1',
        options=[
            {'label': 'Open', 'value': 'Open'},
            {'label': 'High', 'value': 'High'},
            {'label': 'Low', 'value': 'Low'},
            {'label': 'Closing Price', 'value': 'closing_price'},
            {'label': 'Volume', 'value': 'volume'},
            {'label': 'Dividends', 'value': 'Dividends'},
            {'label': 'Stock Splits', 'value': 'Stock_Splits'}
        ],
        value='Open',  # Default value
    ),
    
    # Graph to display real-time line plot for the first column
    dcc.Graph(id='real-time-line-plot-1'),
    dcc.Interval(
        id='interval-component-1',
        interval=3 * 1000,  # in milliseconds
        n_intervals=0
    ),
    
    # Dropdown to select a column for the second graph
    dcc.Dropdown(
        id='column-dropdown-2',
        options=[
            {'label': 'Open', 'value': 'Open'},
            {'label': 'High', 'value': 'High'},
            {'label': 'Low', 'value': 'Low'},
            {'label': 'Closing Price', 'value': 'closing_price'},
            {'label': 'Volume', 'value': 'volume'},
            {'label': 'Dividends', 'value': 'Dividends'},
            {'label': 'Stock Splits', 'value': 'Stock_Splits'}
        ],
        value='High',  # Default value
    ),
    
    # Graph to display real-time line plot for the second column
    dcc.Graph(id='real-time-line-plot-2'),
    dcc.Interval(
        id='interval-component-2',
        interval=30 * 1000,  # in milliseconds
        n_intervals=0
    )
])

# Callback to update the real-time line plot for the first column
@app.callback(
    Output('real-time-line-plot-1', 'figure'),
    [Input('column-dropdown-1', 'value'),
     Input('interval-component-1', 'n_intervals')]
)
def update_real_time_line_plot_1(selected_column, n_intervals):
    # Replace 'stock_data' with your actual table name
    query = f"SELECT timestamp, {selected_column} FROM stock_data ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, con=engine)
    
    # Create a real-time line plot using Plotly Express
    fig = px.line(df, x='timestamp', y=selected_column, title=f'Real-time Line Plot of {selected_column}')
    
    return fig

# Callback to update the real-time line plot for the second column
@app.callback(
    Output('real-time-line-plot-2', 'figure'),
    [Input('column-dropdown-2', 'value'),
     Input('interval-component-2', 'n_intervals')]
)
def update_real_time_line_plot_2(selected_column, n_intervals):
    # Replace 'stock_data' with your actual table name
    query = f"SELECT timestamp, {selected_column} FROM stock_data ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, con=engine)
    today = dt.date.today()
    #x_range = [dt.datetime.combine(today, dt.time.min), dt.datetime.combine(today, dt.time.max)]
    latest_timestamp = df['timestamp'].max()
    x_range = [latest_timestamp - timedelta(minutes=30), latest_timestamp]
    
    
    # Create a real-time line plot using Plotly Express
    fig = px.line(df, x='timestamp', y=selected_column, title=f'Real-time Line Plot of {selected_column}', range_x=x_range)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8885)


# In[7]:


import plotly.graph_objects as go
app = dash.Dash(__name__)

# Override the default Dash CSS to change the background color of the entire page
app.layout = html.Div(style={'backgroundColor': 'black'}, children=[
    html.H1("Real-time Line Plot Dashboard", style={'color': 'white'}),
    
    # Dropdown to select a column for the first graph
    dcc.Dropdown(
        id='column-dropdown-1',
        options=[
            {'label': 'Open', 'value': 'Open'},
            {'label': 'High', 'value': 'High'},
            {'label': 'Low', 'value': 'Low'},
            {'label': 'Closing Price', 'value': 'closing_price'},
            {'label': 'Volume', 'value': 'volume'},
            {'label': 'Dividends', 'value': 'Dividends'},
            {'label': 'Stock Splits', 'value': 'Stock_Splits'}
        ],
        value='Open',  # Default value
        style={'color': 'white'}
    ),
    
    # Graph to display real-time line plot for the first column
    dcc.Graph(id='real-time-line-plot-1'),
    dcc.Interval(
        id='interval-component-1',
        interval=3000,  # Update every 3 seconds
        n_intervals=0
    ),
    
    # Dropdown to select a column for the second graph
    dcc.Dropdown(
        id='column-dropdown-2',
        options=[
            {'label': 'Open', 'value': 'Open'},
            {'label': 'High', 'value': 'High'},
            {'label': 'Low', 'value': 'Low'},
            {'label': 'Closing Price', 'value': 'closing_price'},
            {'label': 'Volume', 'value': 'volume'},
            {'label': 'Dividends', 'value': 'Dividends'},
            {'label': 'Stock Splits', 'value': 'Stock_Splits'}
        ],
        value='High',  # Default value
        style={'color': 'white'}
    ),
    
    # Graph to display real-time line plot for the second column
    dcc.Graph(id='real-time-line-plot-2'),
    dcc.Interval(
        id='interval-component-2',
        interval=3000,  # Update every 3 seconds
        n_intervals=0
    )
])

# Callback to update the real-time line plot for the first column
@app.callback(
    Output('real-time-line-plot-1', 'figure'),
    [Input('column-dropdown-1', 'value'),
     Input('interval-component-1', 'n_intervals')]
)
def update_real_time_line_plot_1(selected_column, n_intervals):
    # Replace 'stock_data' with your actual table name
    query = f"SELECT timestamp, {selected_column} FROM stock_data ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, con=engine)
    
    # Create a real-time line plot using Plotly Express
    fig = px.line(df, x='timestamp', y=selected_column, title=f'Real-time Line Plot of {selected_column}')
    
    # Calculate rolling average using pandas
    window_size = 5  # Adjust the window size as needed
    df['Rolling_Avg'] = df[selected_column].rolling(window=window_size).mean()
    
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Rolling_Avg'], mode='lines', name=f'Rolling Avg ({window_size} points)'))
    
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white')
    
    return fig

# Callback to update the real-time line plot for the second column
@app.callback(
    Output('real-time-line-plot-2', 'figure'),
    [Input('column-dropdown-2', 'value'),
     Input('interval-component-2', 'n_intervals')]
)
def update_real_time_line_plot_2(selected_column, n_intervals):
    # Replace 'stock_data' with your actual table name
    query = f"SELECT timestamp, {selected_column} FROM stock_data ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, con=engine)
    
    # Create a real-time line plot using Plotly Express
    fig = px.line(df, x='timestamp', y=selected_column, title=f'Real-time Line Plot of {selected_column}')
    
    # Calculate rolling average using pandas
    window_size = 5  # Adjust the window size as needed
    df['Rolling_Avg'] = df[selected_column].rolling(window=window_size).mean()
    
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Rolling_Avg'], mode='lines', name=f'Rolling Avg ({window_size} points)'))
    
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=9995)


# In[8]:




app = dash.Dash(__name__)

# Override the default Dash CSS to change the background color of the entire page
app.layout = html.Div(style={'backgroundColor': 'black'}, children=[
    html.H1("Real-time Financial Analysis Dashboard", style={'color': 'white'}),
    
    # Dropdown to select a column for the first graph
    dcc.Dropdown(
        id='column-dropdown-1',
        options=[
            {'label': 'Open', 'value': 'Open'},
            {'label': 'High', 'value': 'High'},
            {'label': 'Low', 'value': 'Low'},
            {'label': 'Closing Price', 'value': 'closing_price'},
            {'label': 'Volume', 'value': 'volume'},
            {'label': 'Dividends', 'value': 'Dividends'},
            {'label': 'Stock Splits', 'value': 'Stock_Splits'}
        ],
        value='Open',  # Default value
        style={'color': 'black'}
    ),
    
    # Graph to display real-time line plot for the first column
    dcc.Graph(id='real-time-line-plot-1'),
    dcc.Interval(
        id='interval-component-1',
        interval=3000,  # Update every 3 seconds
        n_intervals=0
    ),
    
    # Dropdown to select a column for the second graph
    dcc.Dropdown(
        id='column-dropdown-2',
        options=[
            {'label': 'Open', 'value': 'Open'},
            {'label': 'High', 'value': 'High'},
            {'label': 'Low', 'value': 'Low'},
            {'label': 'Closing Price', 'value': 'closing_price'},
            {'label': 'Volume', 'value': 'volume'},
            {'label': 'Dividends', 'value': 'Dividends'},
            {'label': 'Stock Splits', 'value': 'Stock_Splits'}
        ],
        value='High',  # Default value
        style={'color': 'black'}
    ),
    
    # Graph to display real-time line plot for the second column
    dcc.Graph(id='real-time-line-plot-2'),
    dcc.Interval(
        id='interval-component-2',
        interval=3000,  # Update every 3 seconds
        n_intervals=0
    ),
    
    # Candlestick chart
    dcc.Graph(id='candlestick-chart'),
    dcc.Interval(
        id='interval-component-3',
        interval=3000,  # Update every 3 seconds
        n_intervals=0
    ),
    
    # Volume chart
    dcc.Graph(id='volume-chart'),
    dcc.Interval(
        id='interval-component-4',
        interval=3000,  # Update every 3 seconds
        n_intervals=0
    ),
    
      # RSI chart
    dcc.Graph(id='rsi-chart'),
    dcc.Interval(
        id='interval-component-5',
        interval=3000,  # Update every 3 seconds
        n_intervals=0
    )

])
















# Callback to update the real-time line plot for the first column
@app.callback(
    Output('real-time-line-plot-1', 'figure'),
    [Input('column-dropdown-1', 'value'),
     Input('interval-component-1', 'n_intervals')]
)
def update_real_time_line_plot_1(selected_column, n_intervals):
    # Replace 'stock_data' with your actual table name
    query = f"SELECT timestamp, {selected_column} FROM stock_data ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, con=engine)
    
    # Create a real-time line plot using Plotly Express
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df[selected_column], mode='lines', name=selected_column))
    
    # Calculate rolling average using pandas
    window_size = 5  # Adjust the window size as needed
    df['Rolling_Avg'] = df[selected_column].rolling(window=window_size).mean()
    
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Rolling_Avg'], mode='lines', name=f'Rolling Avg ({window_size} points)'))
    
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white', title=f'Real-time Line Plot of {selected_column}')
    
    return fig

# Callback to update the real-time line plot for the second column
@app.callback(
    Output('real-time-line-plot-2', 'figure'),
    [Input('column-dropdown-2', 'value'),
     Input('interval-component-2', 'n_intervals')]
)
def update_real_time_line_plot_2(selected_column, n_intervals):
    # Replace 'stock_data' with your actual table name
    query = f"SELECT timestamp, {selected_column} FROM stock_data ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, con=engine)
    
    
    today = dt.date.today()
    #x_range = [dt.datetime.combine(today, dt.time.min), dt.datetime.combine(today, dt.time.max)]
    latest_timestamp = df['timestamp'].max()
    x_range = [latest_timestamp - timedelta(hours=24), latest_timestamp]
    
    
    # Create a real-time line plot using Plotly Express
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df[selected_column], mode='lines', name=selected_column))
    
    # Calculate rolling average using pandas
    window_size = 5  # Adjust the window size as needed
    df['Rolling_Avg'] = df[selected_column].rolling(window=window_size).mean()
    
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['Rolling_Avg'], mode='lines', name=f'Rolling Avg ({window_size} points)'))
    
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white', title=f'Real-time Line Plot of {selected_column}', xaxis_range=x_range)
    
    return fig

# Callback to update the candlestick chart
@app.callback(
    Output('candlestick-chart', 'figure'),
    [Input('interval-component-3', 'n_intervals')]
)
def update_candlestick_chart(n_intervals):
    # Replace 'stock_data' with your actual table name
    query = "SELECT timestamp, Open, High, Low, closing_price FROM stock_data ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, con=engine)
    
    fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['closing_price'])])
    
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white', title='Candlestick Chart')
    
    return fig

# Callback to update the volume chart
@app.callback(
    Output('volume-chart', 'figure'),
    [Input('interval-component-4', 'n_intervals')]
)
def update_volume_chart(n_intervals):
    # Replace 'stock_data' with your actual table name
    query = "SELECT timestamp, volume FROM stock_data ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, con=engine)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['timestamp'], y=df['volume'], name='Volume'))
    
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white', title='Volume Chart')
    
    return fig


# Callback to update the RSI chart
@app.callback(
    Output('rsi-chart', 'figure'),
    [Input('interval-component-5', 'n_intervals')]
)
def update_rsi_chart(n_intervals):
    # Replace 'stock_data' with your actual table name
    query = "SELECT timestamp, closing_price FROM stock_data ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, con=engine)
    
    # Calculate RSI using pandas_ta library
    import pandas_ta as ta
    df['RSI'] = ta.rsi(df['closing_price'])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['RSI'], mode='lines', name='RSI'))
    
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white', title='Relative Strength Index (RSI)')
    
    return fig

















if __name__ == '__main__':
    app.run_server(debug=True, port=9995)


# In[ ]:




