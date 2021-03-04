import base64
import io

import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf
# yahoo finance / pandas
from pandas_datareader import data as pdr
yf.pdr_override()  # <== that's all it takes :-)

WEEKLY_TRADING_DAYS = 5
YEARLY_TRADING_DAYS = 250
TICKER_MAX_LENGTH = 4

"""
Args:
    ticker: String inputted from user on finance.html route
returns: 
    Dictionary with ticker properties and pandas dataframe of last 252 days trading data
"""


def get_ticker_data(ticker: str) -> {}:
    # validate ticker based on string properties
    if not ticker or (len(ticker) > TICKER_MAX_LENGTH):
        return None
    # make sure we can get trading data for ticker
    if (trading_data := pdr.get_data_yahoo(ticker)).empty:
        return {}
    # print(ticker_props)
    # print(ticker_props.info)
    # print(ticker_props.financials)
    # print(ticker_props.recommendations)
    # print(ticker_props.calendar)


    # download dataframe
    # data = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")
    return {'properties': yf.Ticker(ticker), 'trading_data': trading_data}


def plot_ticker_data(trading_data, ticker_name):
    # create image and pass to submitted_finance html template.
    img = io.BytesIO()
    plt.figure(figsize=(10, 10))
    # plt.plot(data.index, data['Close'])
    # plt.xlabel("date")
    # plt.ylabel("$ price")
    mpf.plot(trading_data.tail(YEARLY_TRADING_DAYS), type='candle', volume=True,
             savefig=img,
             title=f'\n{ticker_name.upper()} Historical Data',
             ylabel_lower='Shares\nTraded')
    # plt.title(f'{ticker} Stock Price:')
    # plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()
