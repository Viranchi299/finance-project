from unittest import TestCase

from website import ticker_parsing


class Test(TestCase):

    def setUp(self) -> None:
        self.valid_ticker_data = ticker_parsing.get_ticker_data('AAPL')

    """
    Passing invalid ticker should return None.
    """

    def test_get_ticker_invalid(self):
        self.assertIsNone(ticker_parsing.get_ticker_data('CCC'))

    """
    Valid ticker, should have dictionary filled with both ticker_props and trading data
    """

    def test_get_ticker_valid(self):
        self.assertIsNotNone(self.valid_ticker_data)
        self.assertIsNotNone(self.valid_ticker_data['properties'])
        self.assertIsNotNone(self.valid_ticker_data['trading_data'])


    """
    For a valid ticker, we should get a dataframe back that we can subset with last 250 trading days since we 
    display this on the HTML template. 
    """


    def test_get_ticker_valid_tradingdata(self):
        self.assertEqual(ticker_parsing.YEARLY_TRADING_DAYS,
                         len(self.valid_ticker_data['trading_data'].tail(ticker_parsing.YEARLY_TRADING_DAYS)))

    """
    Should get back a plot image when passing in a valid ticker. 
    """

    def test_plot_ticker_data(self):
        self.assertIsNotNone(ticker_parsing.plot_ticker_data(self.valid_ticker_data['trading_data'], 'AAPL'))
