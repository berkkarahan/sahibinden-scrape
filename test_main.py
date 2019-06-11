from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.io import IO
from s_scrape.srequests import URLlib, URLreq, URLsln

import time
import datetime

now = datetime.datetime.now()
day = now.day
month = now.month
year = now.year
suffix = str(day)+"-"+str(month)+"-"+str(year)

listingswait = 5
mainwait = 15

ulib = URLlib()
ureq = URLreq()

#print("Currently loading listings from pre-scraped list...")
mscr = MainPageScraper(8, uutils=ulib, lowerdelay=1, upperdelay=2)
print("Scraping started...")
mscr.scrapeModels()
print("Main car models scraped...")
mscr.scrapeSubModels()
print("Sub car models scraped...")
print("Waiting %d seconds before scraping listings..." %listingswait)
time.sleep(listingswait)
mscr.scrapeListings()
IO.pickle_dump("listings_"+suffix+".pkl", mscr.listings)
IO.save_list("listings_"+suffix+".txt", mscr.listings)
scr = DetailsScraper(mscr.listings, 16, ureq, lowerdelay=3, upperdelay=8)
print("Waiting %d seconds before scraping listings..." %mainwait)
time.sleep(mainwait)
scr.scrapeDetails()
IO.pickle_dump("listings_list_"+suffix+".pkl", scr.final_list)
print("Scraping & pickling complete.")
