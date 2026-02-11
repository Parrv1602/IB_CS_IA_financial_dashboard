from StockIndexData import *
import pandas as pd

'''Calculates moving averages'''
def moving_averages(ticker):
    type = st.selectbox("Choose type of MA", ["Simple", "Exponential"])

    if type == "Simple":
        timeframe = st.selectbox("Choose timeframe (days)", ["20", "50", "200"])
        # Must be integer in rolling parameter
        timeframe = int(timeframe)

        sma = ticker["Close"].rolling(timeframe).mean()
        return sma

    elif type == "Exponential":
        timeframe = st.selectbox("Choose timeframe (days)", ["12", "26", "50", "100", "200"])

        # Must be integer in span parameter
        timeframe = int(timeframe)
        ema = ticker["Close"].ewm(span=timeframe, adjust=False).mean().dropna()
        return ema


def relative_strength_index(ticker, window=14):
    delta = ticker["Close"].diff(1).dropna()
    loss = delta.copy()
    gain = delta.copy()

    # Don't need unfitting data, e.g.: -ve cannot be in gain
    gain[gain < 0] = 0
    loss[loss > 0] = 0

    # Absolute value
    gain_ewm = gain.ewm(com=window-1, adjust=False).mean()
    loss_ewm = abs(loss.ewm(com=window-1, adjust=False).mean())

    RS = gain_ewm / loss_ewm
    RSI = 100 - (100/(1.0 + RS))
    RSI = RSI.iloc[5:]
    return RSI


def avg_true_range(ticker):

    #Calculating true range
    ticker["High_low"] = ticker["High"] - ticker["Low"]
    ticker["High_prev_close"] = abs(ticker["High"] - ticker["Close"].shift(1))
    ticker["Low_prev_close"] = abs(ticker["Low"] - ticker["Close"].shift(1))

    ticker["True Range"] = ticker[['High_low', 'High_prev_close', 'Low_prev_close']].max(axis=1)

    atr_type = st.selectbox("Choose type of ATR", ATR_types)
    period=14

    if atr_type == "rma":
        ticker["ATR"] = ticker["True Range"].ewm(alpha=1/period, adjust=False).mean()

    elif atr_type == "sma":
        ticker["ATR"] = ticker["True Range"].rolling(window=period).mean()

    elif atr_type == "ema":
        ticker["ATR"] = ticker["True Range"].ewm(span=period, adjust=False).mean()

    elif atr_type == "wma":
        weights = pd.Series(range(1, period + 1))
        ticker["ATR"] = ticker["True Range"].rolling(window=period).apply(lambda x: (weights*x).sum() / weights.sum(), raw=True)

    return ticker["ATR"].dropna()


def vwap(ticker):

    # Calculate as a series, not a dataframe, cannot calculate with dataframe
    typical_price = ticker["High"].astype(float).squeeze()
    typical_price += ticker["Low"].astype(float).squeeze()
    typical_price += ticker["Close"].astype(float).squeeze()
    typical_price /= 3

    Volume = ticker["Volume"].astype(float).squeeze()

    # Cumulative typical volume
    ticker["Cumsum TP Volume"] = (typical_price * Volume).cumsum()
    ticker["Cumulative Volume"] = ticker["Volume"].cumsum()

    # VWAP
    ticker["VWAP"] = ticker["Cumsum TP Volume"]/ ticker["Cumulative Volume"]

    return ticker

