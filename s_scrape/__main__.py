import time
from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.utils import IO

def _mainruntime(njobs=4,method_submodel='runtime', chunkify = True, wait = 10):

    mscr = MainPageScraper(njobs)
    print("Scraping started...")
    mscr.scrapeModels()
    print("Main car models scraped...")
    mscr.scrapeSubModels(method = method_submodel)
    print("Sub car models scraped...")
    print("Waiting %d seconds before scraping listings..." %wait)
    time.sleep(wait)
    if chunkify:
        listings = mscr.batch_scrapeListings()
    else:
        listings = mscr.scrapeListings()
    IO.save_list("listings.txt",listings)
    scr = DetailsScraper(listings, njobs)
    print("Waiting %d seconds before scraping listings..." %wait)
    time.sleep(wait)
    if chunkify:
        scr.batch_scrapeDetails()
    else:
        scr.scrapeDetails()
    return scr.final_list


def _threading(njobs=4, wait = 10):
    print("Total threads: %s"%str(njobs))
    mscr = MainPageScraper(njobs)
    print("Scraping started...")
    mscr.scrapeModels()
    print("Main car models scraped...")
    mscr.scrapeSubModels()
    print("Sub car models scraped...")
    print("Waiting %d seconds before scraping listings..." %wait)
    time.sleep(wait)
    mscr.scrapeListings()
    IO.save_list("listings.txt", mscr.listings)
    scr = DetailsScraper(mscr.listings, njobs)
    print("Waiting %d seconds before scraping listings..." %wait)
    time.sleep(wait)
    scr.scrapeDetails()
    return scr.final_list


def _using_saved_listings(njobs=4):
    listings = IO.load_list("listings.txt")
    scr = DetailsScraper(listings, njobs)
    scr.scrapeDetails()
    return scr.final_list


if __name__ == "__main__":

    #results = _threading(njobs=128, wait = 10)
    results = _using_saved_listings(njobs=128)

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
