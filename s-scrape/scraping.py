from .base import Scraper
from .utils import URLutils

from bs4 import BeautifulSoup
from multiprocessing import Pool


class MainPageScraper(Scraper):
    def __init__(self):
        super().__init__("https://www.sahibinden.com/kategori/otomobil")
        self._modelurls = []
        self._listings = []

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
    def _get_listings_from_page(self, url):
        print("----> Scraping listings from url: %s" % (url))
        c = URLutils.delayedreadURL(url, 0.5, 1)
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
        with Pool(8) as pool:
            for mainlink in self.linklist:
                for pagingoffset in range(0, 990, 20):
                    link = mainlink + str(pagingoffset)
                    pool.apply_async(self._get_listings_from_page, args=(link,), callback=self._listings.append)
            pool.close()
            pool.join()
        print("Listings scraped succesfully...")


class DetailsScraper():
    def __init__(self, listings):
        self.listings = listings

        self.final_list = []

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
        c = URLutils.delayedreadURL(url, 0.5, 1)

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

    @classmethod
    def _addtoList(self, x):
        print("****PRINTING SCRAPED CAR DETAILS****")
        print(x)
        self.final_list.append(x)
        print(" * Printing length of final list: %i * " % (len(self.final_list)))
        print("************************************")

    def scrapeDetails(self):
        with Pool(8) as pool:
            results = pool.map(self._get_details_from_url,self.listings)
        self.final_list = results

