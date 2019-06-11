from s_scrape.base import Scraper, xpathSafeRead
from s_scrape.io import IO

# scraping
from bs4 import BeautifulSoup
from lxml import html

import re
import sys
import threading

#quick workaround
#from s_scrape.srequests import URLreq as URLutils
#uutils = URLutils()

class MainPageScraper(Scraper):
    def __init__(self, n_jobs, uutils, lowerdelay=1, upperdelay=5):
        super().__init__(url="https://www.sahibinden.com/kategori/otomobil", njobs = n_jobs, lowerdelay=lowerdelay, upperdelay=upperdelay)
        self._modelurls = []
        self.submodelurls = []
        self._listings = []
        self.n_jobs = n_jobs
        self.uutils = uutils
        self.lock = threading.Lock()

    @property
    def linklist(self):
        return self._modelurls

    @property
    def listings(self):
        return self._listings

    #Private methods
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
            #listings_list = []
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
                    self._listings.append(ret_str)
                    self.lock.release()
                except:
                    print('Read error in: ' + str(i))

            return listings_list

        except:
            pass

    def _get_listings_upperlimit(self, link):
        try:
            c = self.uutils.readURL(link)
            xpth = '//*[@id="searchResultsSearchForm"]/div/div[4]/div[1]/div[1]/div/div[1]/span'
            xpth = '//*[@id="searchResultsSearchForm"]/div/div[4]/div[1]/div[2]/div/div[1]/span'

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

    def _wrapperBatchRun_upperlimits(self):
        flat_list = IO.flatten_list(self.submodelurls)
        links = []

        for mainlink in flat_list:
            if mainlink is None:
                continue
            else:
                upperlimit = self._get_listings_upperlimit(mainlink)
                print("Upperlimit for link: %s   -->   is %s" % (mainlink, str(upperlimit)))
                for pagingoffset in range(0, upperlimit + 10, 20):
                    link = mainlink + "?pagingOffset=" + str(pagingoffset)
                    links.append(link)
        return links

    def _wrapperBatchRun_appendlistings(self, url):
        #self._listings.append(self._get_listings_from_page(url))
        self._get_listings_from_page(url)

    def _wrapperBatchRun_scrapeModels(self, car):
        tmp = car.find("a", href=True)
        self._modelurls.append("https://www.sahibinden.com" + tmp['href'] + "?pagingOffset=")

    #Public methods
    def scrapeModels(self):
        c = self.uutils.readURL(self.link)
        soup = BeautifulSoup(c, "html.parser")
        ctgList = soup.find_all("ul", {"class": "categoryList"})
        carList = ctgList[0].find_all("li")
        self.batchrun(self._wrapperBatchRun_scrapeModels, carList)

    def _wrapperBatchRun_scrapeSubModels(self,url):
        self.submodelurls.append(self._get_submodels_from_page(url))

    def scrapeSubModels(self):
        self.batchrun(self._wrapperBatchRun_scrapeSubModels, self._modelurls)
        #if method == 'runtime':
        #    with Pool(self.n_jobs) as pool:
        #        self.submodelurls = pool.map(self._get_submodels_from_page, self._modelurls)
        #elif method == 'test':
        #    with Parallel(n_jobs=self.n_jobs, backend="threading") as Parl:
        #        self.submodelurls = Parl(delayed(self._get_submodels_from_page)(url) for url in self._modelurls)
        #elif method == 'sequential':
        #    submodels = []
        #    for url in self._modelurls:
        #        submodels.append(self._get_submodels_from_page(url))
        #    self.submodelurls = submodels

    def scrapeListings(self):
        links = self._wrapperBatchRun_upperlimits()
        self.batchrun(self._wrapperBatchRun_appendlistings,links)

class DetailsScraper(Scraper):
    def __init__(self, listings, n_jobs, uutils, lowerdelay=1, upperdelay=5):
        super().__init__(url="", njobs=n_jobs, lowerdelay=lowerdelay, upperdelay=5)
        self.listings = listings
        self.final_list = []
        self.n_jobs = n_jobs
        self.uutils=uutils

        #Xpath references for posting details
        self.ilan_xpath = '//*[@id="classifiedId"]'
        self.ilantarihi_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[2]/span'
        self.marka_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[3]/span'
        self.seri_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[4]/span'
        self.model_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[5]/span'
        self.yil_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[6]/span'
        self.yakit_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[7]/span'
        self.vites_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[8]/span'
        self.km_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[9]/span'
        self.kasatipi_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[10]/span'
        self.motorgucu_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[11]/span'
        self.motorhacmi_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[12]/span'
        self.cekis_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[13]/span'
        self.renk_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[14]/span'
        self.garanti_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[15]/span'
        self.hasar_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[16]/span'
        self.plakauyruk_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[17]/span'
        self.kimden_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[18]/span'
        self.takas_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[19]/span'
        self.durum_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[20]/span'

        self.fiyat_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/h3'

    def _get_details_from_url_xpath(self, url):

        car = {}
        print("----> Using xpath for scraping from url: %s" % url)
        c = self.uutils.delayedreadURL(url, self.lowerdelay, self.upperdelay)
        try:
            root = html.fromstring(c)

            # car['clsid'] = root.xpath(self.ilan_xpath)[0].text.strip()
            # car['IlanTarihi'] = root.xpath(self.ilantarihi_xpath)[0].text.strip()
            # car['Marka'] = root.xpath(self.marka_xpath)[0].text.strip()
            # car['Seri'] = root.xpath(self.seri_xpath)[0].text.strip()
            # car['Model'] = root.xpath(self.model_xpath)[0].text.strip()
            # car['Yil'] = root.xpath(self.yil_xpath)[0].text.strip()
            # car['Yakit'] = root.xpath(self.yakit_xpath)[0].text.strip()
            # car['Vites'] = root.xpath(self.vites_xpath)[0].text.strip()
            # car['Km'] = root.xpath(self.km_xpath)[0].text.strip()
            # car['Motor Gucu'] = root.xpath(self.motorgucu_xpath)[0].text.strip()
            # car['Motor Hacmi'] = root.xpath(self.motorhacmi_xpath)[0].text.strip()
            # car['Cekis'] = root.xpath(self.cekis_xpath)[0].text.strip()
            # #car['Kapi'] = root.xpath(self.kapi_xpath)[0].text.strip() #kapi xpath not defined
            # car['Renk'] = root.xpath(self.renk_xpath)[0].text.strip()
            # car['Garanti'] = root.xpath(self.garanti_xpath)[0].text.strip()
            # car['Hasar Durumu'] = root.xpath(self.hasar_xpath)[0].text.strip()
            # car['Plaka / Uyruk'] = root.xpath(self.plakauyruk_xpath)[0].text.strip()
            # car['Kimden'] = root.xpath(self.kimden_xpath)[0].text.strip()
            # car['Takas'] = root.xpath(self.takas_xpath)[0].text.strip()
            # car['Durumu'] = root.xpath(self.durum_xpath)[0].text.strip()
            # car['Fiyat'] = root.xpath(self.fiyat_xpath)[0].text.strip()

            car['clsid'] = xpathSafeRead(root, self.ilan_xpath, 'ilan.')
            car['IlanTarihi'] = xpathSafeRead(root, self.ilantarihi_xpath, 'ilan tarihi.')
            car['Marka'] = xpathSafeRead(root, self.marka_xpath, 'marka.')#root.xpath(self.marka_xpath)[0].text.strip()
            car['Seri'] = xpathSafeRead(root, self.seri_xpath, 'seri.')
            car['Model'] = xpathSafeRead(root, self.model_xpath, 'model.')
            car['Yil'] = xpathSafeRead(root, self.yil_xpath, 'yil.')
            car['Yakit'] = xpathSafeRead(root, self.yakit_xpath, 'yakit.')
            car['Vites'] = xpathSafeRead(root, self.vites_xpath, 'vites')
            car['Km'] = xpathSafeRead(root, self.km_xpath, 'km.')
            car['Motor Gucu'] = xpathSafeRead(root, self.motorgucu_xpath, 'motor gucu.')
            car['Motor Hacmi'] = xpathSafeRead(root, self.motorhacmi_xpath, 'motor hacmi.')
            car['Cekis'] = xpathSafeRead(root, self.cekis_xpath, 'cekis.')
            # #car['Kapi'] = root.xpath(self.kapi_xpath)[0].text.strip() #kapi xpath not defined
            car['Renk'] = xpathSafeRead(root, self.renk_xpath, 'renk.')
            car['Garanti'] = xpathSafeRead(root, self.garanti_xpath, 'garanti.')
            car['Hasar Durumu'] = xpathSafeRead(root, self.hasar_xpath, 'hasar durumu.')
            car['Plaka / Uyruk'] = xpathSafeRead(root, self.plakauyruk_xpath, 'plaka/uyruk.')
            car['Kimden'] = xpathSafeRead(root, self.kimden_xpath, 'kimden.')
            car['Takas'] = xpathSafeRead(root, self.takas_xpath, 'takas.')
            car['Durumu'] = xpathSafeRead(root, self.durum_xpath, 'durumu.')
            car['Fiyat'] = xpathSafeRead(root, self.fiyat_xpath, 'fiyat.')

            print(car)
            print(" **** Processing complete **** ")
            return car
        except:
            print(sys.exc_info()[0], " occured.")

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
        c = self.uutils.delayedreadURL(url, self.lowerdelay, self.upperdelay)

        try:
            soup = BeautifulSoup(c, "html.parser")
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

    def _batch_get_details_xpath(self, links):
        cars = []
        for link in links:
            cars.append(self._get_details_from_url_xpath(link))
        return cars

    def _wrapperBatchRun(self, url):
        self.final_list.append(self._get_details_from_url_xpath(url))

    def scrapeUrl(self, url, method='xpath'):
        if method=='xpath':
            return self._get_details_from_url_xpath(url)
        elif method =='soup':
            return self._get_details_from_url(url)

    def _old_scrapeDetails(self):
        #hotfix!
        finlist = []
        for itm in self.listings:
            if type(itm) == list:
                for j in itm:
                    finlist.append(j)
            else:
                finlist.append(itm)
        self.batchrun(self._wrapperBatchRun, finlist)

    def scrapeDetails(self):
        '''from random import shuffle
        l = shuffle(self.listings)'''
        #random shuffle doesnt work right now
        self.batchrun(self._wrapperBatchRun, self.listings)

    def scrapeDetails2(self):
        from s_scrape.utils import flatten
        from random import shuffle
        fl = flatten(self.listings)
        fl = shuffle(fl)
        self.batchrun(self._wrapperBatchRun, fl)
