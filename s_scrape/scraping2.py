from s_scrape.base import Scraper, xpathSafeRead
from s_scrape.io import IO

# scraping
from bs4 import BeautifulSoup
from lxml import html

import re
import sys
import threading

from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partialmethod

class MainScraper():
    def __init__(self, n_jobs, uutils, lowerdelay=1, upperdelay=5):
        self._mainpage = "https://www.sahibinden.com/kategori/otomobil"
        self.n_jobs = n_jobs
        self.uutils = uutils
        self.lowerdelay = lowerdelay
        self.upperdelay = upperdelay
        self.lock = threading.Lock()
        self.main_modelurls = []
        self.submodels = []
        self.bottom_links = []
        self.listings_list = []


    def _get_submodels_from_page(self, url, url_delayed=True):
        #sublist = list()
        print("----> Scraping sub-models from url: %s" % (url))
        if url_delayed:
            c = self.uutils.delayedreadURL(url, self.lowerdelay, self.upperdelay)
        else:
            c = self.uutils.readURL(url)
        soup = BeautifulSoup(c, "html.parser")
        subList = soup.find_all("li", {"class": "cl3"})

        for itm in subList:
            tmp = itm.find("a", href=True)
            if tmp['href'] != "#":
                ret_str = "https://www.sahibinden.com" + tmp['href']
                self.lock.acquire()
                self.submodels.append(ret_str)
                self.lock.release()
        return sublist

    def _get_listings_from_page(self, url, url_delayed=True):
        if url is None:
            pass
        try:
            print("----> Scraping listings from url: %s" % (url))
            listings_list = []
            if url_delayed:
                c = self.uutils.delayedreadURL(url, self.lowerdelay, self.upperdelay)
            else:
                c = self.uutils.readURL(url)
            soup = BeautifulSoup(c, "html.parser")
            listitems = soup.find_all("tr", {"class": "searchResultsItem"})

            for i in range(len(listitems)):
                try:
                    cur = listitems[i]
                    a_curr = cur.a
                    print('Link posting: ' + a_curr['href'])
                    ret_str = "https://www.sahibinden.com" + a_curr['href']
                    #listings_list.append(ret_str)
                    self.lock.acquire()
                    self.listings_list.append(ret_str)
                    self.lock.release()
                except:
                    print('Read error in: ' + str(i))
        except:
            pass

    def _get_listings_upperlimit(self, link):
        try:
            c = self.uutils.readURL(link)
            xpth = '//*[@id="searchResultsSearchForm"]/div/div[4]/div[1]/div[1]/div/div[1]/span'

            tot = self.uutils.choosebyXPath(c, xpth)
            tot = tot.replace(".", "")
            tot = re.findall('\d+',tot)
            tot = int(tot[0])
            rem = tot % 20
            tot = tot + rem
            if tot < 20:
                tot = 20
            return min(tot, 980)
        except:
           print("Read error - upperlimit: " + link)
           return 20

    def _build_model_urls(self):
       c = self.uutils.readURL(self._mainpage)
       soup = BeautifulSoup(c, "html.parser")
       ctgList = soup.find_all("ul", {"class": "categoryList"})
       carList = ctgList[0].find_all("li")
       for itm in carList:
           tmp = itm.find("a", href=True)
           self.main_modelurls.append("https://www.sahibinden.com" + tmp['href'] + "?pagingOffset=")

    def _scrape_sub_models(self):
        with ThreadPoolExecutor(self.n_jobs) as executor:
            futures = []
            for murl in self.main_modelurls:
                futures.append(executor.submit(self._get_submodels_from_page(murl)))
            for x in as_completed(futures):
                #print("Submodel-url " + str(x.result() + " added to submodelurls list."))
                continue

    def _scrape_upper_limits(self):
        def listings_upperlimit(url_list):
            for url in url_list:
                if url is None:
                    continue
                else:
                    upperlimit = self._get_listings_upperlimit(url)
                    print("Upperlimit for link: %s   -->   is %s" % (mainlink, str(upperlimit)))
                    for pagingoffset in range(0, upperlimit + 10, 20):
                        link = mainlink + "?pagingOffset=" + str(pagingoffset)
                        self.lock.acquire()
                        self.bottom_links.append(link)
                        self.lock.release()

        with ThreadPoolExecutor(self.n_jobs) as executor:
            futures = []
            for surl in self.submodels:
                futures.append(executor.submit(listings_upperlimit, surl))
            for x in as_completed(futures):
                #print("Bottom-link url " + str(x.result()) + " added to bottom_links list.")
                continue

    def preScraping(self):
        self._build_model_urls()
        self._scrape_sub_models()

    def scrapeListings(self):
        self._scrape_upper_limits()
        with ThreadPoolExecutor(self.n_jobs) as executor:
            futures = []
            for burl in self.bottom_links:
                futures.append(executor.submit(self._get_listings_from_page, burl))
            for x in as_completed(futures):
                #print("Bottom-link url " + str(x.result()) + " added to bottom_links list.")
                continue
