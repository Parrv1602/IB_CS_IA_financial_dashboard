from ReturnsCalculations import *
import yfinance as yf
import pandas as pd
import plotly.express as px
from StockIndexData import data

@fetch_data
def simple_returns(ticker_close, start_date, end_date, ticker_name, index_data, index_name):

    # Convert index to a column, proper date access
    index_data = index_data.iloc[1:].reset_index().rename(columns={'index':'Date', index_data.columns[-1]: index_name})
    ticker_close = ticker_close.iloc[1:].reset_index().rename(columns={"index":"Date", ticker_close.columns[-1]: ticker_name})

    graph_data = pd.merge(ticker_close, index_data, on="Date", how="inner")
    fig = px.line(graph_data, x="Date", y=[ticker_name, index_name])
    st.plotly_chart(fig)


@fetch_data2
def logarithmic_returns(ticker_log, start_date, end_date, ticker_name, index_log, index_name):

    index_data = index_log.iloc[1:].reset_index().rename(columns={'index': 'Date', index_log.columns[-1]: index_name})
    ticker_data = ticker_log.iloc[1:].reset_index().rename(columns={"index": "Date", ticker_log.columns[-1]: ticker_name})

    graph_data = pd.merge(ticker_data, index_data, on="Date", how="inner")
    fig = px.line(graph_data, x="Date", y=[ticker_name, index_name])
    st.plotly_chart(fig)


@fetch_data3
def cagr(ticker, index_name, start_date, end_date):

    n = (end_date - start_date).days/365.25

    if n < 1:
        st.write("CAGR is annualised, dates must be at least 1 year apart")
    else:
        CAGR = ((((ticker.iloc[-1] / ticker.iloc[0]) ** (1 / n)) - 1)*100).item()
        CAGR = f"{CAGR:.2f}%"
        st.subheader(f"CAGR: {CAGR}")


@fetch_data3
def alpha(ticker_close, index_name, start_date, end_date):

    #Pandas series uses label based indexing
    if end_date > start_date:
        index = data(index_name, start_date, end_date)
        index_close = index["Close"]

        # Risk-free return
        us_bond = yf.download("^TNX", start=start_date, end=end_date)

        # Strip the data to get yield
        Bond_start = us_bond["Close"]
        if not us_bond.empty:
            # Requires [0][0] to get the value
            bond_yield = (Bond_start.iloc[0][0])/100
            st.write(f"Bond yield (Risk free return): {bond_yield:.2f}")

            # Preparing data for beta calculation
            stock_returns = ticker_close.pct_change().dropna()
            index_return = index_close.pct_change().dropna()


            # Creating a single dataframe
            combined_dataset = pd.concat([stock_returns, index_return], axis=1, join="inner")
            combined_dataset.columns = ["Stock Returns", "Index Returns"]
            combined_dataset.dropna(inplace=True)

            covariance = combined_dataset.cov()

            # Covariance between stock and market
            stock_cov = covariance.loc["Stock Returns", "Index Returns"]
            Index_cov = covariance.loc["Index Returns", "Index Returns"]

            # Beta
            beta = stock_cov / Index_cov
            st.write(f"Beta {beta:.4f}")

            #CAPM
            trading_days = 252
            risk_free_daily_rate = bond_yield / trading_days
            index_returns = combined_dataset["Index Returns"].mean()

            expected_daily_return = risk_free_daily_rate + (beta * (index_returns - risk_free_daily_rate))

            CAPM_annualised = (1+ expected_daily_return)**trading_days - 1

            CAPM = CAPM_annualised.round(2)
            st.write(f"CAPM: {CAPM}")

            #Refered to Gemini for calculation since there was a minor error
            # Alpha = Avg stock return - expected return (CAPM)
            average_daily_stock_return = combined_dataset["Stock Returns"].mean()

            # Annualize actual stock Return by compounding
            annualized_stock_return = (1 + average_daily_stock_return) ** trading_days - 1
            st.write(f"Stock Returns (Annualized Actual Return): {annualized_stock_return:.4f}%")

            # Alpha calculation: Actual Annualized Return - Expected Annualized Return
            alpha_value = annualized_stock_return - CAPM_annualised
            st.subheader(f"Alpha: {alpha_value:.4f}")


        else:
            st.write("No bond yield for these dates")

    else:
        st.write("Start date must be earlier than end date")


