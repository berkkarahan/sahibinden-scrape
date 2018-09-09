import urllib
import random
import time
import pickle

from lxml import html
from requests import get, post
from selenium import webdriver

class URLutils():

        self.user_agent_list = [
            # Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (X11; Linuxlistings =  x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            # Firefox
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

        self.slndrivers = [
            webdriver.Chrome()
        ]

    def _standard_readURL(self, url):
        try:
            random_user_agent = random.choice(self.user_agent_list)
            headers = {'User-Agent': random_user_agent}
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            return response.read()
        except:
            if url is None:
                print('Url is none.')
            else:
                print('Failed requesting url: ' + url)
            pass

    def _pixlr(self, url):
        if not url[-1:] == '/':
            url = url + '/'
        return get('https://pixlr.com/proxy/?url='+url, headers = {'Accept-Encoding' : 'gzip'}, verify=False).text

    def _code_beautify(url):
        headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept':'text/plain, */*; q=0.01',
        'Accept-Encoding':'gzip',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin' : 'https://codebeautify.org',
        'Connection' : 'close'
        }
        return post('https://codebeautify.com/URLService', headers=headers, data='path=' + url, verify=False).text

    def _photopea(url):
        return get('https://www.photopea.com/mirror.php?url=' + url, verify=False).text

    def readURL(self, url, mode='standard'):
        if mode == 'standard':
            return self._standard_readURL(url)
        elif mode == 'api':
            try:
                response = random.choice([self._pixlr, self._code_beautify, self._photopea])(url)
                return response
            except:
                print("APIs failed, falling back to default request mode.")
                return self._standard_readURL(url)
        elif mode == 'selenium':
            drv = random.choice(self.slndrivers)
            drv.get(url)
            return drv.page_source

    def delayedreadURL(self, url, lower_limit, upper_limit, mode='standard'):
        time.sleep(random.uniform(lower_limit,upper_limit))
        return self.readURL(url, mode)

    def choosebyXPath(self,page_content,xpath):
        root = html.fromstring(page_content)
        return root.xpath(xpath)[0].text

class IO():

    @staticmethod
    def save_list(fname, list_name):
        with open(fname,'w') as f:
            for l in list_name:
                f.write("%s\n" % l)

    @staticmethod
    def load_list(fname):
        loaded = []
        with open(fname,'r') as f:
            for line in f:
                loaded.append(line)
        return loaded

    @staticmethod
    def pickle_dump(fname,objname):
        with open(fname, 'wb') as f:
            pickle.dump(objname, f)

    @staticmethod
    def pickle_load(fname):
        with open(fname, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def flatten_list(inp_list):
        return_list = []
        for sublist in inp_list:
            for item in sublist:
                return_list.append(item)
        return return_list
