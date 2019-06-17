import threading
import time
import sys
import random
import requests
from lxml import html

class Scraper():
    def __init__(self,
                url="",
                njobs=4,
                upperdelay = 0.8,
                lowerdelay = 0.5):
        self._link = url
        self._njobs = njobs

        #Delay limits for delayedreadURL
        self.upperdelay = upperdelay
        self.lowerdelay = lowerdelay

    @property
    def link(self):
        return self._link

    def chunks(self, l, njobs):
        # For item i in a range that is a length of l,
        for i in range(0, len(l), njobs):
            # Create an index range for l of n items:
            yield l[i:i+njobs]


    def _threader(self, func, urllist):
        threads = []
        #initialize threads
        for url in urllist:
            task = threading.Thread(target=func, args=(url,), daemon=True)
            threads.append(task)
        #start threads
        for thread in threads:
            thread.start()
        #wait for all to finish
        for thread in threads:
            thread.join()
        #delete all threads
        del threads[:]


    def batchrun(self, func, links):
        links = list(links)
        for begin in range(0, len(links), self._njobs):
            end = begin + self._njobs
            splitted = links[begin:end]
            self._threader(func, splitted)
            progress = end
            if progress > len(links):
                progress = len(links)


class URLrequests():
    def __init__(self, bypassdelayed=False):
        self.bypassdelayed=bypassdelayed

    def _facebook(self, url):
        return requests.get('https://developers.facebook.com/tools/debug/echo/?q=' + url, verify=False).text

    def _code_beautify(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://codebeautify.org',
            'Connection': 'close',
        }
        return requests.post('https://codebeautify.com/URLService', headers=headers, data='path=' + url, verify=False).text

    def _photopea(self, url):
        return requests.get('https://www.photopea.com/mirror.php?url=' + url, verify=False).text

    def _apireadURL(self, url):
        apilist = [self._facebook, self._code_beautify, self._photopea]
        upper = random.randint(0, len(apilist))
        #while apilist and request_not_succesful:
        for _ in range(0,len(apilist)):
            idx = random.randint(0, upper)
            upper = random.randint(0, len(apilist))
            try:
                content = apilist[idx](url)
                break
            except:
                apilist.pop(idx)
        return content


    def readURL(self, url):
        try:
            return self._readURL(url)
        except:
            if url is None:
                print('Url is none.')
            else:
                print('Failed requesting url: ' + url)
            pass

    def delayedreadURL(self, url, lower_limit, upper_limit):
        if self.bypassdelayed:
            return self._readURL
        else:
            time.sleep(random.uniform(lower_limit,upper_limit))
            return self.readURL(url)

    def choosebyXPath(self, page_content, xpath):
        root = html.fromstring(page_content)
        return root.xpath(xpath)[0].text


def xpathSafeRead(pageroot, xpath, field):
    try:
        return pageroot.xpath(xpath)[0].text.strip()
    except:
        print("Encountered ", sys.exc_info(), " while reading field: ", field)
        return 'NA'
