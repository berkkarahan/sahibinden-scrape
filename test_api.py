from s_scrape.base import URLrequests
from s_scrape.srequests import URLlib
import requests

api = URLrequests()

url = 'https://stackoverflow.com/questions/627435/how-do-i-remove-an-element-from-a-list-by-index-in-python'

api.apireadURL(url)

u = URLlib()

u.readURL(url)

requests.get('https://www.photopea.com/mirror.php?url=' + url, verify=False).text

from s_scrape.api import routed

r = routed(url)
r
