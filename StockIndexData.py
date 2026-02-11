import yfinance as yf
import streamlit as st

Global_indexes = ["SP500","Nasdaq 100", "FTSE 100", "STOXX Europe 50", "DAX 40", "Nikkei 225", "Hang Seng", "SENSEX"]
Global_tickers = ["^GSPC", "^IXIC", "^FTSE", "^STOXX50E", "^GDAXI", "^N225", "^HSI", "^BSESN"]

index_to_yf = {
    "SP500" : "^GSPC",
    "Nasdaq 100" : "^IXIC",
    "FTSE 100" : "^FTSE",
    "STOXX Europe 50" : "^STOXX50E",
    "DAX 40" : "^GDAXI",
    "Nikkei 225" : "^N225",
    "Hang Seng" : "^HSI",
    "SENSEX":"^BSESN",
}

#Using wikipedia for ticker list may break when multiple requests take place

SP500_list = sp500_tickers = [
    "MMM", "AOS", "ABT", "ABBV", "ACN", "ADBE", "AMD", "AES", "AFL", "A",
    "APD", "ABNB", "AKAM", "ALB", "ARE", "ALGN", "ALLE", "LNT", "ALL", "GOOGL",
    "GOOG", "MO", "AMZN", "AMCR", "AEE", "AAL", "AEP", "AXP", "AIG", "AMT",
    "AWK", "AMP", "AME", "AMGN", "APH", "ADI", "ANSS", "AON", "APA", "AAPL",
    "AMAT", "APTV", "ACGL", "ADM", "ANET", "AJG", "AIZ", "T", "ATO", "ADSK",
    "ADP", "AZO", "AVB", "AVY", "AXON", "BKR", "BALL", "BAC", "BBWI", "BAX",
    "BDX", "BRK-B", "BBY", "BIO", "TECH", "BIIB", "BLK", "BX", "BA", "BKNG",
    "BWA", "BXP", "BSX", "BMY", "AVGO", "BR", "BRO", "BF-B", "BG", "CHRW",
    "CDNS", "CZR", "CPT", "CPB", "COF", "CAH", "KMX", "CCL", "CARR", "CTLT",
    "CAT", "CBOE", "CBRE", "CDW", "CE", "COR", "CNC", "CNP", "CDAY", "CF",
    "CHTR", "CVX", "CMG", "CB", "CHD", "CI", "CINF", "CTAS", "CSCO", "C",
    "CFG", "CLX", "CME", "CMS", "KO", "CTSH", "CL", "CMCSA", "CMA", "CAG",
    "COP", "ED", "STZ", "CEG", "COO", "CPRT", "GLW", "CTVA", "CSGP", "COST",
    "CTRA", "CCI", "CSX", "CMI", "CVS", "DHI", "DHR", "DRI", "DVA", "DE",
    "DAL", "XRAY", "DVN", "DXCM", "FANG", "DLR", "DFS", "DIS", "DG", "DLTR",
    "D", "DPZ", "DOV", "DOW", "DTE", "DUK", "DD", "DXC", "EMN", "ETN",
    "EBAY", "ECL", "EIX", "EW", "EA", "ELV", "LLY", "EMR", "ENPH", "ETR",
    "EOG", "EPAM", "EQT", "EFX", "EQIX", "EQR", "ESS", "EL", "ETSY", "EG",
    "EVRG", "ES", "EXC", "EXPE", "EXPD", "EXR", "XOM", "FFIV", "FDS", "FICO",
    "FAST", "FRT", "FDX", "FITB", "FSLR", "FE", "FIS", "FI", "FLT", "FMC",
    "F", "FTNT", "FTV", "FOXA", "FOX", "BEN", "FCX", "GRMN", "IT", "GEHC",
    "GEN", "GNRC", "GD", "GE", "GIS", "GM", "GPC", "GILD", "GL", "GPN",
    "GS", "HAL", "HIG", "HAS", "HCA", "PEAK", "HSIC", "HSY", "HES", "HPE",
    "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HWM", "HPQ", "HUM", "HBAN",
    "HII", "IBM", "IEX", "IDXX", "ITW", "ILMN", "INCY", "IR", "PODD", "INTC",
    "ICE", "IFF", "IP", "IPG", "INTU", "ISRG", "IVZ", "INVH", "IQV", "IRM",
    "JBHT", "JBL", "JKHY", "J", "JNJ", "JCI", "JPM", "JNPR", "K", "KDP",
    "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KHC", "KR", "LHX", "LH",
    "LRCX", "LW", "LVS", "LDOS", "LEN", "LIN", "LYV", "LKQ", "LMT", "L",
    "LOW", "LULU", "LYB", "MTB", "MRO", "MPC", "MKTX", "MAR", "MMC", "MLM",
    "MAS", "MA", "MTCH", "MKC", "MCD", "MCK", "MDT", "MRK", "META", "MET",
    "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MRNA", "MHK", "MOH", "TAP",
    "MDLZ", "MPWR", "MNST", "MCO", "MS", "MOS", "MSI", "MSCI", "NDAQ", "NTAP",
    "NFLX", "NEM", "NWSA", "NWS", "NEE", "NKE", "NI", "NDSN", "NSC", "NTRS",
    "NOC", "NCLH", "NRG", "NUE", "NVDA", "NVR", "NXPI", "ORLY", "OXY", "ODFL",
    "OMC", "ON", "OKE", "ORCL", "OTIS", "PCAR", "PKG", "PANW", "PARA", "PH",
    "PAYX", "PAYC", "PYPL", "PNR", "PEP", "PFE", "PCG", "PM", "PSX", "PNW",
    "PXD", "PNC", "POOL", "PPG", "PPL", "PFG", "PG", "PGR", "PLD", "PRU",
    "PEG", "PTC", "PSA", "PHM", "QRVO", "PWR", "QCOM", "DGX", "RL", "RJF",
    "RTX", "O", "REG", "REGN", "RF", "RSG", "RMD", "RVTY", "RHI", "ROK",
    "ROL", "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC", "SLB", "STX", "SRE",
    "NOW", "SHW", "SPG", "SWKS", "SJM", "SNA", "SO", "LUV", "SWK", "SBUX",
    "STT", "STLD", "STE", "SYK", "SYF", "SNPS", "SYY", "TMUS", "TROW", "TTWO",
    "TPR", "TRGP", "TGT", "TEL", "TDY", "TFX", "TER", "TSLA", "TXN", "TXT",
    "TMO", "TJX", "TSCO", "TT", "TDG", "TRV", "TRMB", "TFC", "TYL", "USB",
    "UDR", "ULTA", "UNP", "UAL", "UPS", "URI", "UNH", "UHS", "VLO", "VTR",
    "VRSN", "VRSK", "VZ", "VRTX", "VFC", "VTRS", "VICI", "V", "VMC", "WRB",
    "WAB", "WBA", "WMT", "DIS", "WBD", "WM", "WAT", "WEC", "WFC", "WELL",
    "WST", "WDC", "WRK", "WY", "WHR", "WMB", "WTW", "GWW", "WYNN", "XEL",
    "XYL", "YUM", "ZBRA", "ZBH", "ZTS"
]



Nasdaq_100 = ["MSFT", "NVDA", "AAPL", "GOOGL", "AMZN"]

STOXX_50 = ["ASML.AS", "MC.PA", "SAP.DE", "TTE.PA"]

FTSE_100 =["SHEL.L", "AZN.L", "HSBA.L", "ULVR.L", "REL.L"]

DAX_40 = ["SAP.DE", "SIE.DE", "DTE.DE", "ALV.DE", "AIR.DE"]

Nikkei_225 = ["7203.T", "6758.T", "8306.T", "9984.T", "6501.T"]

Hang_Seng = ["0700.HK", "1299.HK", "0005.HK", "9988.HK", "0939.HK"]

SENSEX = ["RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "BHARTIARTL.NS"]

#Indicator list
Indicators = ["Moving Average (MA)", "Average True Range (ATR)", "Relative Strength Index (RSI)",
              "Volume Weighted Average Price (VWAP)"]

ATR_types = ["rma", "sma", "ema", "wma"]

Index_currency_dict = {"SP500":"$",
                       "Nasdaq 100":"$",
                       "FTSE 100":"GBX (pence)",
                       "STOXX Europe 50":"€",
                       "DAX 40":"€",
                       "Nikkei 225":"¥",
                       "Hang Seng":"HKD",
                       "SENSEX":"₹"}

# Only get data when needed
@st.cache_data
def data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    return df



