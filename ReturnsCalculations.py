import numpy as np
from StockIndexData import *

# Timeframes
Timeframe_dict = {
    "Daily": None,
    "Weekly": "W",
    "Monthly": "M",
    "Yearly": "Y"
}
Years = list(range(2000, 2025))

#Pass the base function as an argument to the decorator
def fetch_data(func):

    #Defining an inner function "wrapper"
    def wrapper(ticker, start_date, end_date, ticker_name, index_data, index_name):

        try:
            # Key to distinguish between different select boxes
            timeframe = st.selectbox("Select Timeframe", Timeframe_dict.keys(), key="simple")

            #Extract only close data to avoid multidimensional error
            ticker_close = ticker["Close"]
            index_close = index_data["Close"]

            if Timeframe_dict[timeframe] is None:
                returns = ticker_close.pct_change() * 100
                index_returns = index_close.pct_change() * 100

            else:
                returns = ticker_close.resample(Timeframe_dict[timeframe]).last().pct_change() * 100
                index_returns = index_close.resample(Timeframe_dict[timeframe]).last().pct_change() * 100

            return func(returns, start_date, end_date, ticker_name, index_returns, index_name)

        except Exception as e:
            st.write(f"Error: {e}")

    return wrapper



def fetch_data2(func):

    def wrapper(ticker, start_date, end_date, ticker_name, index_data, index_name):
        try:
            timeframe = st.selectbox("Select Timeframe", Timeframe_dict.keys(), key="log")

            index_close = index_data[["Close"]].copy()
            ticker_close = ticker[["Close"]].copy()

            if Timeframe_dict[timeframe] is None:
                ticker_log = np.log(ticker_close["Close"] / ticker_close["Close"].shift(1))
                index_log = np.log(index_close["Close"] / index_close["Close"].shift(1))

            else:
                #Users wants specific timeframe log returns data, first resample data, then calculate log returns
                returns = ticker_close.resample(Timeframe_dict[timeframe]).last()
                index = index_data.resample(Timeframe_dict[timeframe]).last()
                ticker_log = np.log(returns["Close"]/returns["Close"].shift(1))
                index_log = np.log(index["Close"]/index["Close"].shift(1))

            return func(ticker_log, start_date, end_date, ticker_name, index_log, index_name)

        except Exception as e:
            st.write(f"{e}")

    return wrapper


def fetch_data3(func):
    def wrapper(ticker, index_name, start_date, end_date):
        try:
            ticker_close = ticker["Close"]

            if ticker_close.empty:
                st.write("Please select different dates")

            return func(ticker_close, index_name, start_date, end_date)

        except Exception as e:
            st.write(f"Error: {e}")

    return wrapper



