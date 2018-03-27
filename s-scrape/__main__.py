import time
from .scraping import DetailsScraper, MainPageScraper
from .utils import IO

#listings = IO.load_list('listings.txt')

if __name__ == "__main__":

    #print("Currently loading listings from pre-scraped list...")
    mscr = MainPageScraper(8)
    print("Scraping started...")
    mscr.scrapeModels()
    print("Main car models scraped...")
    mscr.scrapeSubModels()
    print("Sub car models scraped...")
    print("Waiting 15 seconds before scraping listings...")
    time.sleep(15)
    listings = mscr.scrapeListings()
    IO.save_list("listings.txt",listings)
    scr = DetailsScraper(listings, 8)
    print("Waiting 15 seconds before scraping listings...")
    time.sleep(15)
    scr.scrapeDetails()

    IO.pickle_dump('listings_list.pkl',scr.final_list)
    print("Scraping & pickling complete.")