from s_scrape.utils import IO, URLutils

singleurl = "https://www.sahibinden.com/"
url2 = 'https://www.sahibinden.com/ilan/vasita-otomobil-bmw-2015-4.20d-cabrio-m-sport-ici-kirmizi-boyasiz-603552809'

u = URLutils()

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Read URL
pht = u.testAPI(singleurl,api='ph')
pht
plr = u.testAPI(singleurl,api='pl')
plr
cb = u.testAPI(singleurl,api='cb')
cb

url2
pht2 = u.testAPI(url2)
pht2
