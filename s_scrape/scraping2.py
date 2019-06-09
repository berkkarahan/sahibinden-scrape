from s_scrape.base import Scraper, xpathSafeRead
from s_scrape.io import IO

# scraping
from bs4 import BeautifulSoup
from lxml import html

import re
import sys

from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partialmethod

class MainScraper():
    def __init__(self, n_jobs, uutils, lowerdelay=1, upperdelay=5):
        self._mainpage = "https://www.sahibinden.com/kategori/otomobil"
        self.n_jobs = n_jobs
        self.uutils = uutils
        self.lowerdelay = lowerdelay
        self.upperdelay = upperdelay

    def _get_submodels_from_page(self, url, url_delayed=True):
        sublist = list()
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
                sublist.append(ret_str)
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
                    listings_list.append(ret_str)
                except:
                    print('Read error in: ' + str(i))

            return listings_list

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
       modelurls = []
       for itm in carList:
           tmp = itm.find("a", href=True)
           modelurls.append("https://www.sahibinden.com" + tmp['href'] + "?pagingOffset=")
       return modelurls

    def _scrape_sub_models(self, modelurls):
        submodels = []
        with ThreadPoolExecutor(self.n_jobs) as executor:
            futures = []
            for murl in modelurls:
                futures.append(executor.submit(self._get_submodels_from_page(murl)))
            for x in as_completed(futures):
                submodels.append(x.result())
        return submodels

    def preScraping(self):
        modelurls = self._build_model_urls()
        submodels = self._scrape_sub_models(modelurls)
        return submodels
