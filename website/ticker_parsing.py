import base64
import io

import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf
import pandas as pd
# yahoo finance / pandas
from pandas_datareader import data as pdr

yf.pdr_override()  # <== that's all it takes :-)

WEEKLY_TRADING_DAYS = 5
YEARLY_TRADING_DAYS = 250
TICKER_MAX_LENGTH = 4


def get_ticker_data(ticker: str, num_weeks=2) -> {}:
    """
    :Args:
        ticker: String inputted from user on finance.html route
        num_weeks: default is 2 weeks of trading data
    :return:
        Dictionary with ticker properties and pandas dataframe of last 252 days trading data
    """
    # validate ticker based on string properties
    if not ticker or (len(ticker) > TICKER_MAX_LENGTH) or (not ticker.isalpha()):
        return None
    # make sure we can get trading data for ticker
    if (trading_data := pdr.get_data_yahoo(ticker)).empty:
        return {}
    # print(ticker_props)
    # print(ticker_props.info)
    # print(ticker_props.financials)
    # print(ticker_props.recommendations)
    # print(ticker_props.calendar)
    formatted = pd.DataFrame(trading_data)
    pd.options.display.float_format = '{:,.2f}'.format
    # formatted = formatted.applymap("{0:.2f}".format)

    # data = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")
    return {'properties': yf.Ticker(ticker),
            'trading_data': formatted, 'plot_image': plot_ticker_data(trading_data, ticker),
            'display_data': formatted.tail(WEEKLY_TRADING_DAYS * num_weeks)}


def format_props(ticker_props: {}):
    """
    Format ticker properties passed to submittedfinance.html template displayed in Summary Statistics box.
    """
    pass


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
