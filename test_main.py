from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.io import IO

listingswait = 5
mainwait = 15

#print("Currently loading listings from pre-scraped list...")
mscr = MainPageScraper(256)
print("Scraping started...")
mscr.scrapeModels()
print("Main car models scraped...")
mscr.scrapeSubModels()
print("Sub car models scraped...")
print("Waiting %d seconds before scraping listings..." %listingswait)
time.sleep(listingswait)
mscr.scrapeListings()
IO.save_list("listings.txt",mscr.listings)
scr = DetailsScraper(listings, 64)
print("Waiting %d seconds before scraping listings..." %mainwait)
time.sleep(mainwait)
scr.scrapeDetails(method='test')
