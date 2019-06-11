from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.io import IO
from s_scrape.srequests import URLlib, URLreq, URLsln

import time

ureq = URLlib()

listings = IO.pickle_load('listings.pkl')

finlist = []
for itm in listings:
    if type(itm) == list:
        for j in itm:
            finlist.append(j)
    else:
        finlist.append(itm)

scr = DetailsScraper(finlist, 8, ureq, lowerdelay=2, upperdelay=5)
print("Scraping items from loaded listings...")
scr.scrapeDetails()
results = scr.final_list

print("Using pandas for easier CSV extraction...")
import pandas as pd
import datetime
now = datetime.datetime.now()
day = now.day
month = now.month
year = now.year
suffix = str(day)+"-"+str(month)+"-"+str(year)
#tempfix
df = [x for x in results if x is not None]
df = pd.DataFrame(df)
df.to_csv("listings_"+suffix+".csv", index = False)
