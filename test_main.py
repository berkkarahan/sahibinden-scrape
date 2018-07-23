import time
import itertools
import numpy
from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.utils import IO

listingswait = 5
mainwait = 15

#print("Currently loading listings from pre-scraped list...")
mscr = MainPageScraper(8)
print("Scraping started...")
mscr.scrapeModels()
print("Main car models scraped...")
mscr.scrapeSubModels(method='test')
print("Sub car models scraped...")
print("Waiting %d seconds before scraping listings..." %listingswait)
time.sleep(listingswait)
listings = mscr.scrapeListings(method='test')
IO.save_list("listings.txt",listings)
scr = DetailsScraper(listings, 8)
print("Waiting %d seconds before scraping listings..." %mainwait)
time.sleep(mainwait)
scr.scrapeDetails(method='test')
