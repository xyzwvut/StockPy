import os
import pickle


class Stock:
    """Generic Stock

    TODO:
    - Use dictionary to safe configuration
    """

    class StockNotFoundException(Exception):
        """Stock not in store while looking it up"""
        pass

    class StockAlreadyExistsError(Exception):
        """Tries to create already existing stock"""
        pass


    @staticmethod
    def storage_file_suffix():
        return '.stock'

    @staticmethod
    def stock_directory():
        return './stocks'

    @staticmethod
    def ticker_to_storage_file(sym):
        """Determine the name of the storage file from the WKN"""
        return "%s/%s%s" % (Stock.stock_directory(), sym, Stock.storage_file_suffix())

    @staticmethod
    def already_exists(ticker):
        try:
            with open(Stock.ticker_to_storage_file(ticker), 'rb') as f:
                return True
        except IOError:
            return None

    @staticmethod
    def lookup(ticker):
        """Load the stock from file"""
        # TODO: Not nice
        if Stock.already_exists(ticker):
            with open(Stock.ticker_to_storage_file(ticker), 'rb') as f:
                return pickle.load(f)
        else:
            raise Stock.StockNotFoundException, "Stock not available"


    def __init__(self, ticker, wkn, name, stock_exchange):
        # Avoid double creation of the same stock.
        if Stock.already_exists(ticker):
            raise Stock.StockAlreadyExistsError, "Stock already exists can not create again"

        self.ticker = ticker
        self.wkn = wkn
        self.name = name
        self.stock_exchange = stock_exchange

        self.daily_notations = {}


    def remove(self):
        """Remove stock from disk and memory"""
        # TODO:
        # - Remove from indices
        # - Remove from
        try:
            os.remove(self.ticker_to_storage_file(self.ticker))
        except OSError:
            pass

        del self

    def __str__(self):
        """Pretty print representation of a Stock"""
        s = "tick: %s, wkn: %s, name:%s, exch: %s dn:%s\n" % (self.ticker, self.wkn, self.name, self.stock_exchange, len(self.daily_notations))

        for k in self.daily_notations:
            s = s + " " + str(self.daily_notations[k]) + "\n"
        s = s.rstrip('\n')
        return s

    def has_date(self, date):
        """Is stock price tracked for a given date"""
        return self.dates.has_key(date)

    def storage_file(self):
        """Backing file used for the stock safed on disk"""
        return Stock.ticker_to_storage_file(self.ticker)

    def persist(self):
        """Write the stock to its backing store file"""
        with open(self.storage_file(), "wb") as f:
            pickle.dump(self, f)


class StockFetcher:
    """Fetch the stock from web.  Hide different page souces"""
    def __init__(self, stock):
        self.stock = stock

    def fetch_interval(self, start_date, end_date):
        if start_date > end_date:
            error_message = 'Invalid timespan specified {0} .. {1}'.format(start_date, end_date)
            raise ValueError, error_message

        raise NotImplementedError, "Implement fetch interval"

    def fill_history(self):
        """Fill historic data for stock"""
        raise NotImplementedError, "Implement fetch all history for a stock"
        pass

    def fetch_date(self, date):
        """Fetch stock price on specific date for Stock"""

        if self.stock.has_date(date):
            print "Date already present"
            return

        if not self.date_fetchable(date):
            print "Can not fetch stock for %s" % date
            return False

        # TODO fetch the stock data.
        raise NotImplementedError, "Fetch specific date for a stock"

    def date_fetchable(self, date):
        """Is it possible to fetch notations (daily or intra day) for this date?"""
        return True

    def intraday_fetchable(self, date):
        """Is it possible to fetch intra-day notations for this date?"""

        # Is it fetchable at all?
        if not date_fetchable(self, date):
            return False

        raise NotImplementedError, "Look if its not more than N days back"


class DailyNotation:
    """A notation of a Stock within a Day"""

    def __init__(self, stock, date, op, close, low, high, volume):
        self.stock = stock
        self.date = date
        self.open = op
        self.close = close

        self.low = low
        self.high = high
        self.volume = volume

        # List of Intra day notations. Dict seems a bad idea?
        self.intra_days = {}

    def __str__(self):
        """Pretty print a daily notation"""
        return "%s: o: %s, c:%s, low: %s, hi: %s, vol: %s" % (self.date, self.open, self.close, self.low, self.high, self.volume)

    def _from_csv(self, csv_str):
        """Parse a whole CSV, create multiple StockNotationDaily objects"""
        pass


class IntraDayNotation:
    """A notation of a Stock within a day"""

    def __init__(self, dailyNotation, csv_line):
        self.date = dailyNotation.date

        self.start = None
        self.end = None
        self.open = 0
        self.close = 0
        self.low = 0
        self.high = 0
        self.volume = 0
        self.date = None

        # TODO: Not today, yesterday to N days back
        # Fetch request
        raise NotImplementedError, "Parsing intra-day notation"

