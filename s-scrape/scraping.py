from .base import Scraper
from .base import UPPER_DELAY, LOWER_DELAY
from .utils import URLutils

from bs4 import BeautifulSoup
from multiprocessing import Pool


class MainPageScraper(Scraper):
    def __init__(self, n_jobs):
        super().__init__(url="https://www.sahibinden.com/kategori/otomobil")
        self._modelurls = []
        self._submodelurls = []
        self._listings = []
        self.n_jobs = n_jobs

    @property
    def linklist(self):
        return self._modelurls

    @property
    def listings(self):
        return self._listings

    def scrapeModels(self):

        c = URLutils.readURL(self.link)
        soup = BeautifulSoup(c, "html.parser")
        ctgList = soup.find_all("ul", {"class": "categoryList"})
        carList = ctgList[0].find_all("li")

        for car in carList:
            tmp = car.find("a", href=True)
            self._modelurls.append("https://www.sahibinden.com" + tmp['href'] + "?pagingOffset=")

    @classmethod
    def _get_submodels_from_page(self,url):
        sublist = list()
        print("----> Scraping sub-models from url: %s" % (url))
        c = URLutils.delayedreadURL(url,LOWER_DELAY,UPPER_DELAY)
        soup = BeautifulSoup(c, "html.parser")
        subList = soup.find_all("li", {"class": "cl4"})

        for itm in subList:
            tmp = itm.find("a", href=True)
            if tmp['href'] != "#":
                ret_str = "https://www.sahibinden.com" + tmp['href']
                sublist.append(ret_str)
        return sublist

    def scrapeSubModels(self):
        with Pool(self.n_jobs) as pool:
            self._submodelurls = pool.map(self._get_submodels_from_page, self._modelurls)

    @classmethod
    def _get_listings_from_page(self, url):
        #TODO, check sahibinden.com page structure, can't scrape listings currently
        print("----> Scraping listings from url: %s" % (url))
        c = URLutils.delayedreadURL(url, LOWER_DELAY, UPPER_DELAY)
        soup = BeautifulSoup(c, "html.parser")
        listitems = soup.find_all("tr", {"class": "searchResultsItem"})

        for itm in listitems:
            try:
                tmp = itm.find("a", href=True)
                ret_str = "https://www.sahibinden.com" + tmp['href']
                return ret_str
            except:
                pass

    def scrapeListings(self):
        links = list()

        #flatten submodelurls, list of lists
        flat_list = list()
        for sublist in self._submodelurls:
            for item in sublist:
                flat_list.append(item)

        with Pool(self.n_jobs) as pool:
            for mainlink in flat_list:
                for pagingoffset in range(0, 990, 20):
                    link = mainlink + "?" + str(pagingoffset)
                    links.append(link)
            self._listings = pool.map(self._get_listings_from_page,links)
        print("Listings scraped succesfully...")
        return self._listings

class DetailsScraper(Scraper):
    def __init__(self, listings, n_jobs):
        super().__init__(url="")
        self.listings = listings
        self.final_list = []
        self.n_jobs = n_jobs

    @classmethod
    def _get_details_from_url(self, url):

        list_dict = {0: 'clsid',
                     1: 'IlanTarihi',
                     2: 'Marka',
                     3: 'Seri',
                     4: 'Model',
                     5: 'Yil',
                     6: 'Yakit',
                     7: 'Vites',
                     8: 'Km',
                     9: 'Motor Gucu',
                     10: 'Motor Hacmi',
                     11: 'Cekis',
                     12: 'Kapi',
                     13: 'Renk',
                     14: 'Garanti',
                     15: 'Hasar Durumu',
                     16: 'Plaka / Uyruk',
                     17: 'Kimden',
                     18: 'Takas',
                     19: 'Durumu'}

        print("----> Scraping car post details from url: %s" % (url))
        c = URLutils.delayedreadURL(url, LOWER_DELAY, UPPER_DELAY)

        soup = BeautifulSoup(c, "html.parser")
        try:
            infoList = soup.find_all("ul", {"class": "classifiedInfoList"})
            li = infoList[0].find_all("li")
            fiyat = soup.find_all("div", {"class": "classifiedInfo"})
            fiyat = fiyat[0].find("h3").text.strip()

            car = {}

            for i, res in enumerate(li):
                car[list_dict.get(i)] = res.find("span").text.strip()
            car['Fiyat'] = fiyat
            print(car)
            print(" **** Processing complete **** ")
            return car
        except:
            pass

    def scrapeDetails(self):
        with Pool(self.n_jobs) as pool:
            results = pool.map(self._get_details_from_url,self.listings)
        self.final_list = results

