import time
from .scraping import DetailsScraper
from .utils import IO

listings = IO.load_list('listings.txt')

if __name__ == "__main__":

    print("Currently loading listings from pre-scraped list...")
    scr = DetailsScraper(listings)
    print("Print listings loaded, sleeping 5 seconds before starting scraping... /n")
    time.sleep(5)
    scr.scrapeDetails()

    IO.pickle_dump('listings_list.pkl',scr.final_list)