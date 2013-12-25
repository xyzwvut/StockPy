#!/usr/bin/env python2.7

import argparse
import datetime
import sys

import config

from dateutil import parser

from stock import *


def get_fetch_options(args):
    """Validate arguments of fetch command"""
    args.stock = args.stock.upper()

    if args.end_date < args.start_date:
        error_message = 'Invalid timespan specified {0} .. {1}'.format(args.start_date, args.end_date)
        raise argparse.ArgumentError(None, error_message)

    if args.end_date > datetime.date.today():
        print 'End date in the future. Capping to today.'
        args.end_date = datetime.date.today()

    options = vars(args).copy()

    # TODO: Looks ugly
    if args.intra_day:
        options['fetchtype'] = 'intra-day'
    else:
        options['fetchtype'] = 'daily'

    # TODO: How to define end is set but start isn't?

    return options


def command_fetch(args):
    """Fetch command  'main.py fetch' """

    options = get_fetch_options(args)

    # Print inter vs. intra day fetches
    print 'Fetching {fetchtype} {stock} from {start_date} .. {end_date}'.format(**options)

    # Lookup stock
    stock = Stock.lookup(options['stock'])

    fetcher = StockFetcher(stock)
    fetcher.fetch_interval(options['start_date'], options['end_date'])

    assert False, 'Command Fetch Unimplemented'


def command_prime(args):
    """Initialize with stocks and history data"""
    pass


def mkdate(datestring):
    """Turn a date string into a date object"""
    return parser.parse(datestring, dayfirst=True).date()


def parse_cmdline(argv):
    """Parse commandline"""
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbosity', action='count', help='increase output verbosity')

    subparsers = parser.add_subparsers()

    parser_fetch = subparsers.add_parser('fetch')
    parser_fetch.set_defaults(func=command_fetch)
    parser_fetch.add_argument('stock', help='WKN, ticker name of a stock')

    parser_fetch.add_argument('-s', '--start-date', type=mkdate, default=datetime.date.today(), help='Start date (default today)')
    parser_fetch.add_argument('-e', '--end-date', type=mkdate, default=datetime.date.today(), help='End date (default today)')
    parser_fetch.add_argument('--intra-day', default=None, action='store_true', help='Intra day information')

    args = parser.parse_args(argv)

    return args


def main(argv):
    config.load_config()

    args = parse_cmdline(argv)

    if args.func:
        args.func(args)


if __name__ == '__main__':
    main(sys.argv[1:])
