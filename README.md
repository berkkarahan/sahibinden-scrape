# sahibinden-scrape
A (not so) sloppy sahibinden.com scraper

### Minimal dependencies
- Only BeautifulSoup is required as a third-party library apart from python standard library
    - pages are scraped from xpath using html from lxml package
- ~~joblib package is taken from sklearn.externals~~
- Using built-in parallelization.

## Usage
Running main from command-line uses fully exhaustive scraping, arguement parsing is not yet implemented.
```
python -m s-scrape
```
## TO-DO
- Find a way not to send too many requests.
- Better CLI with arguement parsing.
- Support for storing scraped data into a local database.
- Find a way to not send requests for non-existing pages in sahibinden.com
    - Use maximum number of listings per vehicle as an upper limit.
