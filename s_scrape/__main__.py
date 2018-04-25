import time
from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.utils import IO

#listings = IO.load_list('listings.txt')

if __name__ == "__main__":

    listingswait = 5
    mainwait = 15

    #print("Currently loading listings from pre-scraped list...")
    mscr = MainPageScraper(64)
    print("Scraping started...")
    mscr.scrapeModels()
    print("Main car models scraped...")
    mscr.scrapeSubModels()
    print("Sub car models scraped...")
    print("Waiting %d seconds before scraping listings..." %listingswait)
    time.sleep(listingswait)
    listings = mscr.scrapeListings()
    IO.save_list("listings.txt",listings)
    scr = DetailsScraper(listings, 64)
    print("Waiting %d seconds before scraping listings..." %mainwait)
    time.sleep(mainwait)
    scr.scrapeDetails()

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
        df = [x for x in scr.final_list if x is not None]
        df = pd.DataFrame(df)
        df.to_csv("listings_"+suffix+".csv")
    except:
        IO.pickle_dump('listings_list.pkl', scr.final_list)
        print("Scraping & pickling complete.")