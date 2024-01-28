import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# Create a Streamlit app
st.title('Finance Dashboard')

# User input for selecting tickers
tickers = ('TSLA', 'AAPL', 'MSFT', 'BTC-USD', 'ETH-USD')
selected_tickers = st.multiselect('Pick your assets', tickers)

# Date range selection
start_date = st.date_input('Start', value=pd.to_datetime('2021-01-01'))
end_date = st.date_input('End', value=pd.to_datetime('today'))

# Define a function to calculate relative returns
def calculate_relative_returns(df):
    rel = df.pct_change()
    cum_ret = (1 + rel).cumprod() - 1
    cum_ret = cum_ret.fillna(0)
    return cum_ret

# Fetch and display returns for selected tickers
if len(selected_tickers) > 0:
    data = yf.download(selected_tickers, start=start_date, end=end_date)['Adj Close']
    returns = calculate_relative_returns(data)
    st.header('Returns of {}'.format(selected_tickers))
    st.line_chart(returns)

# EODHD Stock Screener
st.header('EODHD Stock Screener')

# Get the user's API key for EOD Historical Data
api_key = "65278f250ee504.73645246"  # Replace with your actual API key

ticker = st.sidebar.text_input('Ticker', 'AAPL.US')
data_type = st.sidebar.selectbox('Data Type', options=['Fundamental Data', 'Stock News and Sentiment Analysis', 'Live / Delayed Data', 'Sentiment Analysis', 'Upcoming Earnings, Trends, IPOs and Splits', 'Insider Transaction Details'])

if data_type == 'Fundamental Data':
    url = f'https://eodhistoricaldata.com/api/fundamentals/{ticker}?api_token={api_key}&fmt=json'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        financial_data = st.sidebar.selectbox("Financial Data", options=list(data.keys()))

        if financial_data == 'Financials':
            statement = st.sidebar.selectbox('Statement', options=list(data['Financials'].keys()))
            df = pd.DataFrame(data['Financials'][statement]['quarterly'])
        else:
            try:
                df = pd.DataFrame(data[financial_data])
            except:
                df = pd.DataFrame(data[financial_data], index=['index'])
        st.write(df)
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
   
        st.error(f"Response content: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Continue the code for other data types (Stock News, Sentiment Analysis, Upcoming Earnings, Insider Transaction Details)
# import json
# import openai
# import streamlit as st
# import yfinance as yf
# import matplotlib.pyplot as plt
# from ctransformers import AutoModelForCausalLM
# from app import responses


# openai.api_key = open('API_KEY', 'r').read()

# def get_stock_price(ticker):
#     return str(yf.Ticker(ticker).history(period='1d')['Close'][0])

# # Function to calculate SMA (Simple Moving Average)
# def calculate_SMA(ticker, window):
#     data = yf.Ticker(ticker).history(period='1y')['Close']
#     return str(data.rolling(window=window).mean().iloc[-1])

# # Function to calculate EMA (Exponential Moving Average)
# def calculate_EMA(ticker, window):
#     data = yf.Ticker(ticker).history(period='1y')['Close']
#     return str(data.ewm(span=window, adjust=False).mean().iloc[-1])

# # Function to calculate RSI (Relative Strength Index)
# def calculate_RSI(ticker):
#     data = yf.Ticker(ticker).history(period='1y')['Close']
#     delta = data.diff()
#     up = delta.clip(lower=0)
#     down = -1 * delta.clip(upper=0)
#     ema_up = up.ewm(com=14, adjust=False).mean()
#     ema_down = down.ewm(com=14, adjust=False).mean()
#     rs = ema_up / ema_down
#     rsi = 100 - (100 / (1 + rs))
#     return str(rsi.iloc[-1])

# # Function to calculate MACD (Moving Average Convergence Divergence)
# def calculate_MACD(ticker):
#     data = yf.Ticker(ticker).history(period='1y')['Close']
#     short_EMA = data.ewm(span=12, adjust=False).mean()
#     long_EMA = data.ewm(span=26, adjust=False).mean()
#     MACD = short_EMA - long_EMA
#     signal = MACD.ewm(span=9, adjust=False).mean()
#     MACD_histogram = MACD - signal
#     return f'MACD: {MACD.iloc[-1]}, Signal: {signal.iloc[-1]}, Histogram: {MACD_histogram.iloc[-1]}'

# # Function to plot stock price
# def plot_stock_price(ticker):
#     data = yf.Ticker(ticker).history(period='1y')
#     plt.figure(figsize=(10, 5))
#     plt.plot(data.index, data['Close'])
#     plt.title(f'{ticker} Stock Price Over Last Year')
#     plt.xlabel('Date')
#     plt.ylabel('Stock Price ($)')
#     plt.grid(True)
#     plt.savefig('stock.png')
#     plt.close()

# functions = [
#     {
#         'name': 'get_stock_price',
#         'description': 'Gets the latest stock price given the ticker symbol of a company',
#         'parameters': {
#             'type': 'object',
#             'properties': {
#                 'ticker': {
#                     'type': 'string',
#                     'description': 'The stock ticker symbol for a company (for example AAPL for Apple)'
#                 }
#             },
#             'required': ['ticker']
#         }
#     },
#       {
#         'name': 'calculate_SMA',
#         'description': 'calculate the simple moving average for a given strock ticker and a window ',
#         'parameters': {
#             'type': 'object',
#             'properties': {
#                 'ticker': {
#                     'type': 'string',
#                     'description': 'the stock ticker symbol for a company (eg. AAPL for apple)',
#                 },
#                 'window': {
#                     'type': 'integer',
#                     'description': 'the timeframe to consider when calculating the sma '
#                 },
#             },
#             'required': ['ticker' ,'window']
#         }
#     },
#       {
#         'name': 'calculate_EMA',
#         'description': 'calculate the exponential moving average for a given stock ticker and a window',
#         'parameters': {
#             'type': 'object',
#             'properties': {
#                 'ticker': {
#                     'type': 'string',
#                     'description': 'the stock ticker symbol for a company (eg. AAPL for apple)'
#                 },
#                 'window': {
#                     'type': 'integer',
#                     'description': 'the timeframe to consider when calculating the EMA '
#                 },
#             },
#             'required': ['ticker']
#         }
#     },
#       {
#         'name': 'calculate_RSI',
#         'description': 'calculate the RSI for a given stock ticker and a window',
#         'parameters': {
#             'type': 'object',
#             'properties': {
#                 'ticker': {
#                     'type': 'string',
#                     'description': 'the stock ticker symbol for a company (eg. AAPL for apple)'
#                 }
#             },
#             'required': ['ticker']
#         }
#     },
#       {
#         'name': 'calculate_MACD',
#         'description': 'calculate the macd for a given stock ticker  ',
#         'parameters': {
#             'type': 'object',
#             'properties': {
#                 'ticker': {
#                     'type': 'string',
#                     'description': 'the stock ticker symbol for a company (eg. AAPL for apple)'
#                 }
#             },
#             'required': ['ticker']
#         }
#     },
#       {
#         'name': 'plot_stock_price',
#         'description': 'plot the stock pricew for the last year given the ticker symbol of a company ',
#         'parameters': {
#             'type': 'object',
#             'properties': {
#                 'ticker': {
#                     'type': 'string',
#                     'description': 'the stock ticker symbol for a company (eg. AAPL for apple)'
#                 }
#             },
#             'required': ['ticker']
#         }
#     },
# ]



# # Define available functions
# available_functions = {
#     'get_stock_price': get_stock_price,
#     'calculate_SMA': calculate_SMA,
#     'calculate_EMA': calculate_EMA,
#     'calculate_RSI': calculate_RSI,
#     'calculate_MACD': calculate_MACD,
#     'plot_stock_price': plot_stock_price
# }

# # Initialize session state for messages
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []

# # Streamlit app title
# st.title(' Chatbot Assistant')

# # User input textbox
# user_input = st.text_input('Your input:')



# if user_input:
#     try:
#         st.session_state['messages'].append({'role': 'user', 'content': user_input})

#         response = openai.ChatCompletion.create(
#             model='gpt-3.5-turbo',
#             messages=st.session_state['messages'],
#             functions=functions,
#             function_call='auto'
#         )

#         response_message = response['choices'][0]['message']

#         if response_message.get('function_call'):
#             function_name = response_message['function_call']['name']
#             function_args = json.loads(response_message['function_call']['arguments'])
#             args_dict = function_args
#             function_to_call = available_functions[function_name]
#             function_response = function_to_call(**args_dict)

#             if function_name == 'plot_stock_price':
#                 st.image('stock.png')
#             else:
#                 st.session_state['messages'].append(response_message)
#                 st.session_state['messages'].append({
#                     'role': 'function',
#                     'name': function_name,
#                     'content': function_response
#                 })

#                 # Additional response from the second model
#                 second_response = openai.ChatCompletion.create(
#                     model='gpt-3.5-turbo-0613',
#                     messages=st.session_state['messages']
#                 )
                
#                 st.text(second_response['choices'][0]['message']['content'])
#                 st.session_state['messages'].append({'role': 'assistant', 'content': second_response['choices'][0]['message']['content']})
#                 responses( second_response['choices'][0]['message']['content'])

#         else:
#             st.text(response_message['content'])
#             st.session_state['messages'].append({'role': 'assistant', 'content': response_message['content']})

#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")
#         st.text(e)