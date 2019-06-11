from s_scrape.scraping import DetailsScraper
from s_scrape.io import IO
from s_scrape.srequests import URLlib, URLreq, URLsln
import itertools

ureq = URLlib()

listings = IO.load_list('listings_10-6-2019.txt')
scr = DetailsScraper(listings, 16, ureq, lowerdelay=3, upperdelay=16)
scr.scrapeDetails()

print(scr.final_list)

try:
    import pandas as pd
    d = pd.DataFrame(scr.final_list)
    d.to_csv("listings.csv")
except:
    IO.pickle_dump("dumped_listings.pkl", scr.final_list)
