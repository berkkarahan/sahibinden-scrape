from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.io import IO
from s_scrape.srequests import URLlib, URLreq, URLsln, APIreq

import time

listingswait = 5
mainwait = 15

ar = APIreq()

#print("Currently loading listings from pre-scraped list...")
mscr = MainPageScraper(16, uutils=ar, lowerdelay=1, upperdelay=2)
print("Scraping started...")
mscr.scrapeModels()
print("Main car models scraped...")
mscr.scrapeSubModels()
print("Sub car models scraped...")
print("Waiting %d seconds before scraping listings..." %listingswait)
time.sleep(listingswait)
mscr.scrapeListings()
IO.pickle_dump("listings.pkl", mscr.listings)
IO.save_list("listings.txt", mscr.listings)
scr = DetailsScraper(mscr.listings, 16, ar, lowerdelay=3, upperdelay=16)
print("Waiting %d seconds before scraping listings..." %mainwait)
time.sleep(mainwait)
scr.scrapeDetails()
