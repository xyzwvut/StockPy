import csv
import re
import requests

from stock import *

class ComDirectMetaData:
    """
    Comdirect metadata to talk to the web page

    file: comdirect.json

    """
    class IdNotationMissmatchException(Exception):
        pass

    def __init__(self):
        self.stock_metadata = {}

    def _fetch_id_notation(self, wkn):
        """Fetch ID_NOTATION for a wkn from web"""

        url = "http://comdirect.de/inf/search/all.html"
        payload = { 'SEARCH_VALUE', wkn }

        r = requests.get(url, params=payload)

        # TODO: Make more robust
        id_notation = re.search('ID_NOTATION=(\S+)"', r.text).group(1)

        return id_notation

    def _add_id_notation(self, wkn, id_notation):
        """Add wkn -> id notation"""

        # Get or create dictionary for wkn
        data = self.stock_metadata.get_key(wkn, {})

        # Get or create entry for ID_NOTATION
        data.get_key('ID_NOTATION', id_notation)

        # Already existed, check equal
        if data['ID_NOTATION'] != id_noation:
            raise ComDirectMetaData.IdNotationMissmatchException

    def get_id_notation(self, wkn):
        """Get ID_NOATAION for wkn by loading from cache or web"""
        try:
            return self.stock_metadata[wkn]['ID_NOTATION']

        except LookupError:
            print 'id-notation not found fetching it'

            id_notation = self._fetch_id_notation(self, wkn)
            self._add_id_notation(self, wkn, id_notation)


class ComDirectFetcher:
    """
    Comdirect uses following URL to fetch data

    http://www.comdirect.de/inf/kursdaten/historic.csv?
        DATETIME_TZ_START_RANGE_FORMATED=30.06.1991
        &ID_NOTATION=24022547
        &random=1371069539572
        &mask=true&INTERVALL=16
        &modal=false
        &DATETIME_TZ_END_RANGE_FORMATED=12.06.2013'
    """
    def __init__(self, stock):
        self.stock = stock

    def fetchInterval(self, start, end):
        """Fetch set of days"""

        # Intra days if possible
        # Remaining days are daylies
        pass

    # Single day requests, what is the start and end date?
    # Are both dates included?
    # WKN to ID-Noation

    values = {
        'DATETIME_TZ_START_RANGE_FORMATED' : '30.06.1991',
        'DATETIME_TZ_END_RANGE_FORMATED' : '12.06.2013',
        'ID_NOTATION' : '24022547',
        'mask' : 'true',
        'INTERVALL' : '16',
        'modal' : 'false',
    }

    def assembleURL(self):
        url = 'http://www.comdirect.de/inf/kursdaten/historic.csv'
        data = urllib.urlencode(values)
        request = urllib2.Request(url, data)
        html_str = response.read()

        print(html_str)

        csv_reader = csv.DictReader(html_str.splitlines(1), delimiter=';')

    def fetch(self):
        """Fetch the file"""
        pass


class ComdirectMapper:
    """Map stocks to comdirect notations.
        Data stored in json files on disk.
        Look them up for translation.
    """
    def __init__(self, stock):
        self.stock = stock

    def pathname(self):
        # TODO: project home directory missing
        return "./comdirect/stock-%s.json" % stock.wkn

    def load_from_file(self):
        pass

    def translate(self, params):
        """Dictionary of params translated"""
        return


class ComDirectDailyCSVReader:
    """Create lots of daily stock prices from CSV string
       The CSV layout is the one provided by ComDirect bank
       General layout

       E.ON SE Namens-Aktien o.N.(WKN: ENAG99 Boerse: Xetra)

       Datum;Zeit;Eroffnung;Hoch;Tief;Schluss;Volumen
       12.06.2013;14:00;12,80;13,045;12,75;12,895;8.363.097,00
       11.06.2013;14:00;12,815;12,86;12,705;12,82;8.375.009,00
       10.06.2013;14:00;12,89;12,975;12,78;12,865;7.291.396,00
       07.06.2013;14:00;12,815;12,98;12,715;12,92;9.584.072,00
       ...
    """

    def __init__(self, stock, raw_csv_str):
        self.stock = stock
        self.raw_csv = raw_csv_str

    def parse_header_line1(self, line):
        """Parse header line 1
           Looks something like:
           E.ON SE Namens-Aktien o.N.(WKN: ENAG99 Borse: Xetra)
        """
        match = re.search(r"(.*)\(WKN:\s+(.*) B.rse:\s+(.*)\)", line)
        # TODO: Is there something better than lastindex?
        if not match or match.lastindex != 3:
            raise IOError, "Malformed CSV header"

        match = re.search(r"(.*)\(WKN:\s+(.*) B.rse:\s+(.*)\)", line)
        # TODO: Is there something better than lastindex?
        if not match or match.lastindex != 3:
            raise IOError, "Faild search on stock's name, wkn, exchange"

        try:
            self.check_name(match.group(1))
            self.check_wkn(match.group(2))
            self.check_stock_exchange(match.group(3))
        except Exception, e:
            print "Failed to check stock's name, WKN, exchange"
            raise

    def parse_header_line2(self, line):
        """Line 2 is empty"""
        if not line == '':
            raise IOError, "Empty line expected"

    def parse_header_line3(self, line):
        """Parse header line 3
            Looks something like:
           (Datum;Zeit;Eroffnung;Hoch;Tief;Schluss;Volumen)
        """
        match = re.search(r"^(Datum;Zeit;Eroffnung;Hoch;Tief;Schluss;Volumen)$", line)
        if not match:
            raise IOError, "Malformed CSV header"

    def consume_day_notation(self, line):
        """Consume a line and turn it into a Daily Notation"""

        elements = line.split(';')
        if len(elements) != 7:
            raise IOError, "Failed sarch daily notation"
        date = elements[0]

        # element[1] is the time
        dn = DailyNotation(self.stock, date, elements[2], elements[3],
                           elements[4], elements[5], elements[6])

        # Add notation to stock.
        self.stock.daily_notations[date] = dn

    def parse_csv(self):
        """Parse the CSV string held in the object"""

        # TODO Be more precise.  Use the class member, consume it line by line.
        # Maybe via a generator.
        splited = self.raw_csv.split('\n', 3)

        self.parse_header_line1(splited[0])
        self.parse_header_line2(splited[1])
        self.parse_header_line3(splited[2])

        # TODO get the stock object
        stock = None

        # Now the rest
        for row in splited[3].splitlines():
            #print row

            # Remove empty lines
            if row == '':
                continue

            self.consume_day_notation(row)

    def check_name(self, str):
        """Check if str is a valid name of a Stock and save it in the object"""
        if self.stock.name != str:
            raise NotImplementedError, "Missmatch on Stock's name"

    def check_wkn(self, str):
        """Check if str is a valid WKN and save it in the object"""
        if self.stock.wkn != str:
            raise NotImplementedError, "Missmatch on WKN"

    def check_stock_exchange(self, str):
        """Check if str is a valid stock exchange and save it in the object"""
        if self.stock.stock_exchange != str:
            raise NotImplementedError, "Missmatch on stock exchange"

    def parse_price(str):
        """Chek if string is a vlaid price and return it as such"""
        # TODO raise expection on error
        pass

    def parse_date(str):
        """Check if string is a valid date and return it as such"""
        # TODO raise exception on error
        pass
