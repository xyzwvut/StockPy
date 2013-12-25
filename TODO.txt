Questions:
- Beautiful soup / requests


Done
- Fetch for a single stock and single day and store it somewhere.
    - Get commandline interface.
        --stock='ticker name'
        --start-date='today' is default
        --end-date='today' is default
        --intra-day
    - Make it a subcommand 'fetch'
    - Write command line option tests
- Migrate to Pytest
- Testing: use artificial stocks and remove them at the end.
- Stock vs. StockFetcher
    - Where to put load from file?
- Add application configuration file
- Resolve cycle creating stock, presisting stock, loading stock


TODO
- Make Stock tests not depend on each other.
- Create StockFile that handles stock serialization onto the disk
- StockFile and general DataFile?
- Fetch history for a single stock.
- Stock vs. StockFetcher
    - Where to make sure that there will be no stocks with the same name.
    - Instantiate ComDirectFetcher and hide it.
        - Try other portal if not available info.
- Add logging support
    - Into a file
    - Set loglevel via -vvv at the commandline
- Get comdirect meta-data to do fetches for stocks.
    - Query website to get detail page of WKN.
    - Search for ID_NOTATION.
    - Store meta-data in a separate file.
    - Write unit tests.
- Cleanup comdirect unit tests.
- Create DataFile class that handles the write back to ...
    - Directory structure.
    - Load on apps start.
- Fetch intra-day data for a day.
- Find out if intra-day data can be fetched.
    - Not later than 30 days.
    - Not today (only if partial is given).
    - If today, then only thil now - 20 minutes.
    - Work day.
- Keep members of an index (DAX, M-DAX, TechDax).
    - Change ofer dates.
    - Join/Leave sets.
    - Each time a member changes, save a new list.
    - Newest takes precedence
    - If different, log changes.
- Comdirect
    - Hide the URL construction.
    - Map generic names (start, end, open, close, vol, high, low)
- Stock
    - Contains WKN, Name, List of capital changes
    - JSON encoding of some example stocks
        - DBK, Thyssen, EON,
- Index


Unit Tests

 ./py.test


Sublime Text Help

Command+P Goto Anything
    When using Goto Anything, you can prefix your query with @ to find a symbol, # to search within a file or : to jump to a line number. Unfortunately, Sublime Text does not search symbols in unopened files.
