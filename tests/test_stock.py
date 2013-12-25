import pytest

from stock import *

class TestStockFactory:
    def test_lookup_missing(self):
        with pytest.raises(Stock.StockNotFoundException):
            stock = Stock.lookup('DUMMY')

    def test_add_stock(self):
        s = Stock("DUMMY", "DUMMY", "Dummy Name", "Xetra")
        s.persist()

    def test_lookup_available(self):
        s = Stock.lookup("DUMMY")

    def test_add_same_stock(self):
        with pytest.raises(Stock.StockAlreadyExistsError):
            s = Stock("DUMMY", "DUMMY", "Dummy Name", "Xetra")

    def test_remove_stock(self):
        s = Stock.lookup("DUMMY")

        s.remove()

        # Make sure really away.
        with pytest.raises(Stock.StockNotFoundException):
            stock = Stock.lookup('DUMMY')

