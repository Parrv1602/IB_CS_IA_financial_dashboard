from ReturnsPlot import *
from GraphPlotting import *
from IndicatorCalculations import *
import streamlit as st
import datetime
from MonteCarloModel import *
# Layout
st.set_page_config(
    page_title = "Financial Dashboard",
    layout="wide"
)

index_name = st.sidebar.selectbox("Select index", Global_indexes, key="Index")

# Initialise to avoid "ticker undefined error"
ticker = None
ticker_name = None

if index_name == "SP500":
    ticker = st.sidebar.selectbox("Select Stock", SP500_list, key="SP500")
    ticker_name = ticker

elif index_name == "Nasdaq 100":
    ticker = st.sidebar.selectbox("Select Stock", Nasdaq_100, key="Nasdaq 100")
    ticker_name = ticker

elif index_name == "FTSE 100":
    ticker = st.sidebar.selectbox("Select Stock", FTSE_100, key="FTSE 100")
    ticker_name = ticker

elif index_name == "STOXX Europe 50":
    ticker = st.sidebar.selectbox("Select Stock", STOXX_50, key="STOXX 50")
    ticker_name = ticker

elif index_name == "DAX 40":
    ticker = st.sidebar.selectbox("Select Stock", DAX_40, key="DAX 40")
    ticker_name = ticker

elif index_name == "Nikkei 225":
    ticker = st.sidebar.selectbox("Select Stock", Nikkei_225, key="Nikkei 225")
    ticker_name = ticker

elif index_name == "Hang Seng":
    ticker = st.sidebar.selectbox("Select Stock", Hang_Seng, key="Hang Seng")
    ticker_name = ticker

elif index_name == "SENSEX":
    ticker = st.sidebar.selectbox("Select Stock", SENSEX, key="SENSEX")
    ticker_name = ticker


start_date = st.sidebar.date_input(label="Select a start date", value="today", min_value=datetime.date(2000, 1, 1))
end_date = st.sidebar.date_input(label="Select end date", max_value="today")

st.sidebar.title("Screens")

#Selection directs user to the chosen screen
options = st.sidebar.selectbox("Choose an screen",["Dashboard", "Risk & Return, and volatility metrics", "Monte Carlo Analysis"])

indicator = st.sidebar.selectbox("Choose an indicator", Indicators, key="indicator")


if ticker == None or ticker_name == None:
    st.subheader("Please select a ticker from the list")
else:
    ticker_data = data(ticker, start_date, end_date)
    if options == "Dashboard":
        indicator_bool = st.selectbox("Display indicator in chart?", ["True", "False"], key="indicator_choice")
        interactive(ticker_data, ticker_name, indicator_bool, indicator)

    elif options == "Risk & Return, and volatility metrics":
        st.header("Risk & Return and Volatility metrics")

        # Daily data
        index_ticker = index_to_yf[index_name]
        index_data = data(index_ticker, start_date, end_date)
        st.write(index_ticker)

        returns_list = ["Simple", "Logarithmic", "CAGR", "Alpha"]
        RandR = st.selectbox("Choose type of returns", returns_list)

        if RandR == "Simple":
            index_close = index_data["Close"]
            simple_returns(ticker_data, start_date, end_date, ticker_name, index_data, index_name)

        elif RandR == "Logarithmic":
            logarithmic_returns(ticker_data, start_date, end_date, ticker_name, index_data, index_name)

        elif RandR == "CAGR":
            cagr(ticker_data, index_name, start_date, end_date)

        elif RandR == "Alpha":
            #Convert index name to ticker name
            index_name = index_to_yf[index_name]
            alpha(ticker_data, index_name, start_date, end_date)


    elif options == "Monte Carlo Analysis":
       #Streamlit executes code from top to bottom, so error handle at the top
       if start_date > end_date or start_date == end_date:
           st.subheader("Choose an end date greater than the start date")
       else:

           st.title("Monte Carlo analysis")
           col1, col2 = st.columns(2)
           close_data = ticker_data["Close"].iloc[-1]
           end_stockPrice = close_data[ticker_name]

           num_simulations = col1.slider("Select the number of simulations", 100, 1000)
           steps = col1.slider(f"Number of days to run the simulation after {end_date}", 1, 100)
           sigma = col2.slider("Select sigma (volatility %)", 0, 100)
           drift = col2.slider("Select risk-free interest rate (%)", 0, 25)

           if steps == 0 or sigma == 0 or drift == 0:
               st.write("To simulate Monte Carlo simulations the above parameters must be greater than 0")
           else:
               #variable in datetime, so extract the days only
               currency = Index_currency_dict[index_name]
               col1.metric(f"Stock price at {end_date}", f"{currency} {np.round(end_stockPrice,2)}")
               num_days = steps
               MCAnalysis = MonteCarloAnalysis(ticker_name, index_name, ticker_data, end_stockPrice, start_date, end_date, num_simulations, sigma, drift, num_days)

               #if MCAnalysis.last_price():
               col2.metric(f"{ticker_name} volatility (%) from {start_date} to {end_date}", np.round(MCAnalysis.actual_vol(),3)*100)
               MCAnalysis.monte_carlo_simulations()
               MCAnalysis.plot_histogram()



