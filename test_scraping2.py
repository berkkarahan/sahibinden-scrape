from s_scrape.srequests import URLlib
from s_scrape.scraping2 import MainScraper

if __name__ == "__main__":
    u = URLlib()
    msc = MainScraper(64, u)
    msc.preScraping()
    # msc.scrapeListings()
