# Level 3, Task 6: Interactive Web Scraping

A practice console application that fetches the first catalog page from [Books to Scrape](https://books.toscrape.com/) and extracts each book's title, price, availability, and star rating. The menu lets you display a chosen number of books, search titles, or exit. A single page request is made per scrape or search.

## Install

Python 3.8 or newer is recommended. Install the dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The request timeout is 10 seconds. The app reports network, timeout, invalid response, and missing field issues in a user-friendly way. Missing book fields are shown as `Unknown`.

## Tests

```bash
python -m unittest -v
```

Unit tests use sample HTML and mocked HTTP requests, so they do not contact the live website.

This application is intended for practice. Always respect the website's terms, robots guidance, rate limits, and other access policies when scraping.
