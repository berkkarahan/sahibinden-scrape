from s_scrape.scraping import DetailsScraper
from s_scrape.utils import IO

listings = IO.load_list('listings.txt')
scr = DetailsScraper(listings, 8)
scr.scrapeDetails()

print(scr.final_list)
