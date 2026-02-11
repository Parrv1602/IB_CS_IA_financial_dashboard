import numpy as np
from StockIndexData import *
import plotly.express as px

class MonteCarloAnalysis():
    def __init__(self, ticker_name, index_name, ticker_data, lastprice, start_date, end_date, num_simulations, sigma, drift, num_days):
        self.ticker_name = ticker_name
        self.index_name = index_name
        self.ticker_data = ticker_data
        self.lastprice = lastprice
        self.start_date = start_date
        self.end_date = end_date
        self.num_simulations = int(num_simulations)
        self.sigma = sigma
        self.drift = drift
        self.num_days = int(num_days)

    def last_price(self):
        #Index based labelling
        try:
            if self.ticker_data.empty:
                st.write(f"No data available for {self.ticker_name}")
            else:
                column = self.ticker_data["Close"]
                lastprice = column[self.ticker_name].iloc[-1]
                return np.round(lastprice,2)

        except Exception as e:
            st.write(f"Unexpected error: {e}")
            return False


    def actual_vol(self):
        close_prices = self.ticker_data["Close"]

        #Use returns when calculating volatility
        log_returns = close_prices.pct_change()
        std = log_returns.std()
        vol = std * np.sqrt(self.num_days)
        return vol

    def monte_carlo_simulations(self):
        #np.zeros expects the following arguments: ((num rows, num columns), dtype= __)
        simulations = np.zeros((self.num_days, self.num_simulations))
        simulations[0] = self.lastprice

        #Using GBM
        mu = self.drift/100
        sigma = self.sigma/100
        T = 1
        steps = self.num_days
        dt = T/252

        for i in range(1, steps):
            # Deterministic trend
            deterministic_term = (mu - 0.5 * sigma ** 2) * dt

            for j in range(self.num_simulations):

                # Random shock is unique to each simulation path
                random_shock = sigma * np.sqrt(dt) * np.random.normal(0, 1)

                #The previous stock price
                S0 = simulations[i-1,j]
                simulations[i,j] = S0*np.exp(deterministic_term + random_shock)
        self.simulations = simulations

        return simulations

    def plot_histogram(self):
        final_prices = self.simulations[-1]
        mean_final_price = np.mean(final_prices)
        fig = px.histogram(final_prices, title=f"Monte Carlo Probability distribution of {self.ticker_name}",template="plotly_white", histnorm="probability density")
        fig.update_traces(xbins=dict(size=3),marker_line_width=0.5)
        fig.add_vline(x=float(mean_final_price), line_dash="dash", line_color="red", annotation_text=f"{self.ticker_name} mean={np.round(float(mean_final_price),2)}")
        fig.update_layout(xaxis_title=f"{self.ticker_name} price")
        st.plotly_chart(fig)







