# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 21:35:10 2018

@author: berk
"""
#python default imports
import urllib
import random
import concurrent.futures
import time
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
#3rd party imports
from bs4 import BeautifulSoup

#start declaring globals
listings = []
linklist = []
list_dict = {0:'clsid',
             1:'IlanTarihi',
             2:'Marka',
             3:'Seri',
             4:'Model',
             5:'Yil',
             6:'Yakit',
             7:'Vites',
             8:'Km',
             9:'Motor Gucu',
             10:'Motor Hacmi',
             11:'Cekis',
             12:'Kapi',
             13:'Renk',
             14:'Garanti',
             15:'Hasar Durumu',
             16:'Plaka / Uyruk',
             17:'Kimden',
             18:'Takas',
             19:'Durumu'}
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
#end declaring globals

#results list
final_list = []

def get_car_models():
    #read car models and urls from the leftside list.
    global linklist
    global user_agent_list
    main_url = "https://www.sahibinden.com/kategori/otomobil"
    
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent':user_agent}
    request = urllib.request.Request(main_url, headers=headers)
    response = urllib.request.urlopen(request)
    c = response.read()
    
    soup = BeautifulSoup(c,"html.parser")
    ctgList = soup.find_all("ul",{"class":"categoryList"})
    carList = ctgList[0].find_all("li")
    
    linklist = []
    for car in carList:
        tmp = car.find("a", href=True)
        linklist.append("https://www.sahibinden.com" + tmp['href']+ "?pagingOffset=")

#helper function for parallelization
def get_listings_from_page(url):
    #provided with the url, gets all possible listings from pages 1 to 50.
    global listings
    
    secs = random.randint(5,20)
    print("Waiting %i secs before sending request for url: %s" % (secs, url))
    time.sleep(secs)
    
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent':user_agent}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    c = response.read()
    
    soup = BeautifulSoup(c, "html.parser")
    listitems = soup.find_all("tr",{"class":"searchResultsItem"})
    
    for itm in listitems:
        try:
            tmp = itm.find("a", href=True)
            listings.append("https://www.sahibinden.com" + tmp['href'])
        except:
            pass 
            
def get_listings_from_models():
    #parallelized
    global listings
    for mainlink in linklist:
        print("Scraping car listings for: "+mainlink)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as exc:
            for pagingoffset in range(0,990,20):
                link = mainlink+str(pagingoffset)
                print("Current link: " + link)
                exc.submit(get_listings_from_page,link)
        print("**** Scraping done, removing duplicates ****")
        listings = list(set(listings))

#save/load listings
def save_list(filename, obj):
    file = open(filename,'w')
    for l in obj:
            file.write("%s\n" % l)

def load_list(filename):
    loaded_listings = []
    with open(filename,'r') as f:
        for line in f:
            loaded_listings.append(line)
    return loaded_listings

def get_details_from_url(url):
    #gets detailed information of cars provided with listing urls.
    global list_dict
    global final_list
    global user_agent_list
    secs = random.randint(5,20)
    print("Waiting %i secs before sending request for url: %s" % (secs, url))
    time.sleep(secs)
    
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent':user_agent}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    c = response.read()
    
    soup = BeautifulSoup(c,"html.parser")
    infoList = soup.find_all("ul",{"class":"classifiedInfoList"})
    li = infoList[0].find_all("li")
    fiyat = soup.find_all("div",{"class":"classifiedInfo"})
    fiyat = fiyat[0].find("h3").text.strip()
    
    car = {}
    
    for i, res in enumerate(li):
        car[list_dict.get(i)] = res.find("span").text.strip()
    car['Fiyat'] = fiyat
    final_list.append(car)
    print(" **** Processing complete **** ")
    print("------->" + url)


def get_details_mp():
    #boom boom pow. SKRAAH SKRAAH.
    global listings
    pool = Pool(cpu_count())
    for link in listings:
        pool.apply_async(get_details_from_url, args = (link,))
    pool.close()
    pool.join()
    print("Scraping complete!!!")
    
def main():
    global listings
    global linklist
    try:
        listings = load_list('listings.txt')
        print("Listings successfuly loaded, getting detailed car informations...")
    except:
        print("Listings not found, trying to load linklist...")
        
    try:
        linklist = load_list('linklist.txt')
        print("Linklist successfuly loaded, extracting listings...")
        get_listings_from_models()
        print("Extracted listings, getting detailed car informations...")
        get_details_mp()
    except:
        print("Linklist not found, making a dry run...")
        
if __name__ == "__main__":
    main()
        