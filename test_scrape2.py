from s_scrape.scraping2 import MainScraper
from s_scrape.io import IO
from s_scrape.srequests import URLlib, URLreq, URLsln, APIreq

import time

listingswait = 5
mainwait = 15

ureq = URLreq()

#print("Currently loading listings from pre-scraped list...")
mscr = MainScraper(8, uutils=ureq, lowerdelay=1, upperdelay=2)
l = mscr.preScraping()
