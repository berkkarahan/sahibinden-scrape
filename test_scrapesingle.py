from s_scrape.utils import IO, URLutils

# scraping
from bs4 import BeautifulSoup
from lxml import html
from multiprocessing import Pool
import re

singleurl = "https://www.sahibinden.com/ilan/vasita-otomobil-audi-sahibinden-audi-a3-sedan-dizel-otomatik-piril-piril-temiz-588976164/detay"

#Read URL
c = URLutils.readURL(singleurl)

#XPath details of sahibinden postings
ilan_xpath = '//*[@id="classifiedId"]'
ilantarihi_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[2]/span'
marka_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[3]/span'
seri_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[4]/span'
model_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[5]/span'
yil_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[6]/span'
yakit_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[7]/span'
vites_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[8]/span'
km_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[9]/span'
kasatipi_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[10]/span'
motorgucu_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[11]/span'
motorhacmi_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[12]/span'
cekis_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[13]/span'
renk_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[14]/span'
garanti_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[15]/span'
hasar_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[16]/span'
plakauyruk_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[17]/span'
kimden_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[18]/span'
takas_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[19]/span'
durum_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/ul/li[20]/span'

fiyat_xpath = '//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/h3'

root = html.fromstring(c)


#dictionary to store scraped details
car = {}

car['clsid'] = root.xpath(ilan_xpath)[0].text.strip()
car['IlanTarihi'] = root.xpath(ilantarihi_xpath)[0].text.strip()
car['Marka'] = root.xpath(marka_xpath)[0].text.strip()
car['Seri'] = root.xpath(seri_xpath)[0].text.strip()
car['Model'] = root.xpath(model_xpath)[0].text.strip()
car['Yil'] = root.xpath(yil_xpath)[0].text.strip()
car['Yakit'] = root.xpath(yakit_xpath)[0].text.strip()
car['Vites'] = root.xpath(vites_xpath)[0].text.strip()
car['Km'] = root.xpath(km_xpath)[0].text.strip()
car['Motor Gucu'] = root.xpath(motorgucu_xpath)[0].text.strip()
car['Motor Hacmi'] = root.xpath(motorhacmi_xpath)[0].text.strip()
car['Cekis'] = root.xpath(cekis_xpath)[0].text.strip()
car['Renk'] = root.xpath(renk_xpath)[0].text.strip()
car['Garanti'] = root.xpath(garanti_xpath)[0].text.strip()
car['Hasar Durumu'] = root.xpath(hasar_xpath)[0].text.strip()
car['Plaka / Uyruk'] = root.xpath(plakauyruk_xpath)[0].text.strip()
car['Kimden'] = root.xpath(kimden_xpath)[0].text.strip()
car['Takas'] = root.xpath(takas_xpath)[0].text.strip()
car['Durumu'] = root.xpath(durum_xpath)[0].text.strip()
car['Fiyat'] = root.xpath(fiyat_xpath)[0].text.strip()

print(car)
