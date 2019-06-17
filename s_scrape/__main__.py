import time
import argparse
import random
from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.io import IO

def _scrape_listings(njobs=4, lowerdelay=1, upperdelay=2, uutils=None):
    print("Total threads: %s"%str(njobs))
    mscr = MainPageScraper(njobs, uutils, lowerdelay=lowerdelay, upperdelay=upperdelay)
    print("Scraping started...")
    mscr.scrapeModels()
    print("Main car models scraped...")
    mscr.scrapeSubModels()
    print("Sub car models scraped...")
    print("Waiting %d seconds before scraping listings..." %(10))
    time.sleep(10)
    mscr.scrapeListings()
    return mscr.listings

def _full_scraper(njobs=4, lowerdelay=1, upperdelay=2, uutils=None):
    print("Total threads: %s"%str(njobs))
    mscr = MainPageScraper(njobs, uutils, lowerdelay=lowerdelay, upperdelay=upperdelay)
    print("Scraping started...")
    mscr.scrapeModels()
    print("Main car models scraped...")
    mscr.scrapeSubModels()
    print("Sub car models scraped...")
    print("Waiting %d seconds before scraping listings..." %(10))
    time.sleep(10)
    mscr.scrapeListings()
    IO.save_list("listings.txt", mscr.listings)
    scr = DetailsScraper(mscr.listings, njobs, uutils, lowerdelay=lowerdelay, upperdelay=upperdelay)
    print("Waiting %d seconds before scraping listings..." %(10))
    time.sleep(10)
    scr.scrapeDetails()
    return scr.final_list


def _using_saved_listings(listloc, njobs=4, uutils=None):
    listings = IO.load_list(listloc)
    scr = DetailsScraper(listings, njobs, uutils, lowerdelay=lowerdelay, upperdelay=upperdelay)
    scr.scrapeDetails()
    return scr.final_list

parser = argparse.ArgumentParser()

parser.add_argument("--lf",help="""Load listings file for pre-scraped listings.""")
parser.add_argument("--lo",help="""Save listings only and exit.""", action='store_true')
parser.add_argument("--wait",help="""Seconds to wait before sending another request.""", type=int)
parser.add_argument("--nworkers",help="""Number of workers for concurrent processing.""", type=int)

args = parser.parse_args()

if __name__ == "__main__":

    from s_scrape.srequests import URLlib
    u = URLlib()

    lowerdelay = max(0,args.wait - random.uniform(1,5))
    upperdelay = min(args.wait + random.uniform(1,5), 10)

    if args.lo:
        listings = _scrape_listings(njobs=args.nworkers,
                                    lowerdelay=lowerdelay,
                                    upperdelay=upperdelay, 
                                    uutils=u)

        print("Listings scraped, saving listings.")
        IO.save_list("listings.txt", listings)
    elif args.lf:
        print("Pre-scraped listings location is given, using list for scraping main details...")
        results = _using_saved_listings(args.lf, njobs=args.nworkers, uutils=u)
    else:
        print("<<<-------Starting full scraper------->>>")
        results = _full_scraper(njobs=args.nworkers,
                                lowerdelay=lowerdelay,
                                upperdelay=upperdelay,
                                uutils=u)

    try:
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
    except:
        IO.pickle_dump('listings_list.pkl', scr.final_list)
        print("Scraping & pickling complete.")
