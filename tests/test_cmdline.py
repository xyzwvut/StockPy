
import pytest
import datetime

from main import parse_cmdline, get_fetch_options

# TODO:
# 1. parse_cmdline()
# 2. How to test for invalid commanlines?
# 3. Assert function called


"""
def test_parse_fetch():
	argv = "fetch"

	args = parse_cmdline(arg)

	assert(False, "Incomplete commandline should not be reached")
"""

def test_parse_fetch_eon():
	argv = ['fetch', 'enag99']

	args = parse_cmdline(argv)

	assert(args.stock == "enag99")
	assert(args.start_date == datetime.date.today())
	assert(args.end_date == datetime.date.today())
	assert(args.intra_day == None)


def test_parse_fetch_start_date():
	argvs = [['fetch','--start-date=1.2.2001', 'enag99'],
			 ['fetch','-s', '1.2.2001', 'enag99']]

	for argv in argvs:
		args = parse_cmdline(argv)

		assert(args.stock == "enag99")
		assert(args.start_date == datetime.date(2001, 2, 1))
		assert(args.end_date == datetime.date.today())


def test_parse_fetch_end_date():
	argvs = [['fetch', '--start-date=2.1.2001', '--end-date=2.3.2001', 'enag99'],
	         ['fetch', '-s', '2.1.2001', '-e', '2.3.2001', 'enag99']]
	
	for argv in argvs:
		args = parse_cmdline(argv)

		assert(args.stock == "enag99")
		assert(args.start_date == datetime.date(2001, 1, 2))
		assert(args.end_date == datetime.date(2001, 3, 2))


def test_parse_fetch_end_date():
	argvs = [['fetch', '--end-date=3.4.2001', 'enag99'],
			 ['fetch', '-e', '3.4.2001', 'enag99']]

	for argv in argvs:
		args = parse_cmdline(argv)

		assert(args.stock == "enag99")
		assert(args.start_date == datetime.date.today())
		assert(args.end_date == datetime.date(2001, 4, 3))


def test_parse_fetch_start_date_formats():
	argv = [ ['fetch', '--start-date=1.2.2001', 'enag99'],
	         ['fetch', '--start-date=2.3.2001', 'enag99'] ]
	date = [datetime.date(2001, 2, 1),
			datetime.date(2001, 3, 2)]

	assert(len(argv) == len(date))

	for idx in range(len(argv)):
		args = parse_cmdline(argv[idx])

		assert(args.stock == "enag99")
		assert(args.start_date  == date[idx])


def test_parse_fetch_intraday():
	argv = ['fetch', '--intra-day', 'enag99']

	args = parse_cmdline(argv)

	assert(args.stock == "enag99")
	assert(args.start_date == datetime.date.today())
	assert(args.end_date == datetime.date.today())
	assert(args.intra_day == True)


def test_parse_fetch_intraday():
	argv = ['fetch', 'enag99']

	args = parse_cmdline(argv)

	assert(args.stock == "enag99")
	assert(args.start_date == datetime.date.today())
	assert(args.end_date == datetime.date.today())
	assert(args.intra_day == None) # TODO: Do we want it this way?


def test_options_fetch():
	argv = ['fetch', 'enag99']

	options = get_fetch_options(parse_cmdline(argv))

	assert(options['stock'] == "ENAG99")
	assert(options['start_date'] == datetime.date.today())
	assert(options['end_date'] == datetime.date.today())
	assert(options['fetchtype'] == 'daily')


def test_options_fetch_intraday():
	argv = ['fetch', '--intra-day', 'enag99']

	options = get_fetch_options(parse_cmdline(argv))

	assert(options['stock'] == "ENAG99")
	assert(options['start_date'] == datetime.date.today())
	assert(options['end_date'] == datetime.date.today())
	assert(options['fetchtype'] == 'intra-day')

