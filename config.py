import os
import ConfigParser

config = ConfigParser.ConfigParser()


def load_config():
    """Load config file"""
    config.readfp(open('defaults.cfg'))
    config.read(['defaults.cfg', os.path.expanduser('~/.stockpy.cfg')])

    update_default_config()


def update_default_config():
    """Update default config file"""

    config = ConfigParser.RawConfigParser()
    config.add_section('main')
    config.set('main', 'foo', 'bar')

    config.add_section('data')
    config.set('data', 'root_dir', 'data')
    config.set('data', 'stock_dir', 'stocks')

    config.add_section('comdirect')
    config.set('comdirect', 'intra_day_span_back', '30')
    config.set('comdirect', 'daily_span_back', '2160')
    config.set('comdirect', 'meta_data_file', 'comdirect_meta')

    with open('default.cfg', 'wb') as configfile:
        config.write(configfile)
