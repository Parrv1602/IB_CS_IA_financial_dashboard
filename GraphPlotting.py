import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IndicatorCalculations import *
from ReturnsCalculations import *
import pandas as pd

#for MA, VWAP
def indicator_graph(indicator_data, indicator_name, fig):
    
    if indicator_name == "Volume Weighted Average Price (VWAP)":
        y_data = indicator_data.iloc[:,7]
    else:
        y_data = indicator_data.iloc[:,0]
    fig.add_trace(go.Scatter(
        x=indicator_data.index,
        y=y_data,
        mode="lines",
        name=indicator_name,
        line=dict(color="blue", width=2),
    ),
        row=1, col=1
    )

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        title=indicator_name
    )

    st.plotly_chart(fig)


def interactive(ticker, ticker_name, indicator_bool, indicator):

    close = ticker["Close"]
    volume = ticker["Volume"]
    high = ticker["High"]
    low = ticker["Low"]
    open = ticker["Open"]

    # Creating a dataframe with OHLCV (Open, High, Low, Close, Volume) columns in the dataframe
    OHLCV = pd.concat([close, volume, high, low, open], axis=1)
    OHLCV.columns = ["Close", "Volume", "High", "Low", "Open"]
    OHLCV.replace([None], "Data unavailable", inplace=True)

    if OHLCV["Close"].isnull().all():
        st.subheader("Choose different dates")

        st.subheader("Or, no data for this ticker, please choose a different ticker")

    # Create plots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3]
    )

    # Any type of chart added after defining add_trace and go
    fig.add_trace(go.Candlestick(

        x=OHLCV.index,
        open=OHLCV["Open"],
        low=OHLCV["Low"],
        high=OHLCV["High"],
        close=OHLCV["Close"]
    ),
        row=1, col=1
    )

    fig.add_trace(go.Bar(
        x=OHLCV.index,
        y=OHLCV["Volume"],
        name="Volume",
    ),
        row=2, col=1
    )

    if indicator_bool == "True":
        if indicator == "Moving Average (MA)":
            indicator_data = moving_averages(ticker)
            indicator_graph(indicator_data, indicator, fig)

        elif indicator == "Relative Strength Index (RSI)":
            indicator_data = relative_strength_index(ticker)

            fig2 = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.7, 0.3]
            )

            fig2.add_trace(go.Scatter(
                x=indicator_data.index,
                y=indicator_data.iloc[:, 0],
                mode="lines",
                name="Indicator",
                line=dict(color="purple", width=2)
            ),
                row=1, col=1
            )
            fig.update_layout(xaxis_rangeslider_visible=False, title=ticker_name, xaxis_title="Date",
                              yaxis_title="Price")
            fig2.update_layout(xaxis_rangeslider_visible=False, title="RSI")
            st.plotly_chart(fig)
            st.plotly_chart(fig2)


        elif indicator == "Average True Range (ATR)":
            indicator_data = avg_true_range(ticker)

            # Cannot use same code as RSI because return data is different
            fig2 = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.7, 0.3]
            )

            fig2.add_trace(go.Scatter(
                x=indicator_data.index,
                y=indicator_data,
                mode="lines",
                name="Indicator",
                line=dict(color="purple", width=2)
            ),
                row=1, col=1
            )

            fig.update_layout(xaxis_rangeslider_visible=False, title=ticker_name, xaxis_title="Date",
                              yaxis_title="Price")

            fig2.update_layout(xaxis_rangeslider_visible=False, title="ATR")
            st.plotly_chart(fig)
            st.plotly_chart(fig2)

        elif indicator == "Volume Weighted Average Price (VWAP)":
            indicator_data = vwap(ticker)
            indicator_graph(indicator_data, indicator, fig)


    elif indicator_bool == "False":
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            xaxis_title="Date", yaxis_title="Price"
        )

        st.plotly_chart(fig)









