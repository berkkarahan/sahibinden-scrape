import threading
import time
import random

class Scraper():
    def __init__(self,
                url="",
                njobs=4,
                urlgetmode='standard',
                upperdelay = 0.8,
                lowerdelay = 0.5):
        self._link = url
        self._njobs = njobs

        #Scraper specific options
        self.urlgetmode = urlgetmode
        #Delay limits for delayedreadURL
        self.upperdelay = upperdelay
        self.lowerdelay = lowerdelay

    @property
    def link(self):
        return self._link

    def chunks(l, njobs):
        # For item i in a range that is a length of l,
        for i in range(0, len(l), njobs):
            # Create an index range for l of n items:
            yield l[i:i+n]


    def _threader(self, func, urllist):
        threads = []
        #initialize threads
        for url in urllist:
            task = threading.Thread(target=func, args=(url,))
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
    def __init__(self):
        pass

    def readURL(self, url):
        return self._readURL(url)

    def delayedreadURL(self, url, lower_limit, upper_limit):
        time.sleep(random.uniform(lower_limit,upper_limit))
        return self.readURL(url)
