# Task 2: Data collection

This folder contains a very simple CLI for scraping historical price data for Brent crude oil, Urals crude oil and Dutch TTF gas. The CLI is used with the following syntax:

```python3 main.py <indicator> <output_file>```

The output_file should have the .csv extension.

### Scraping methods

The data is scraped from three separate web sources. Each request was constructed by visiting those web sources using a standard web browser first, and cloning request headers from the browser. This method is probably not very reliable or resilient to changes in the underlying API. Some of the headers might contain temporary values that will expire (like the &AUTH argument in urals.py). I am also unsure whether sending these requests from a computer other than mine will work. Hopefully the CLI still works on your end nevertheless.

### Data

This CLI collects very simple price data. Each row simply contains a date and a closing price. Other data like highs, lows or volume was available from some sources but not all. This data is simply dropped to keep the output standardized.
