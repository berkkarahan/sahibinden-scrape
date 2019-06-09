import random
from requests import get, post


def routed(url):

    def pixlr(url):
        if not url[-1:] == '/':
            url = url + '/'
        print("Debug: Returning with pixlr.")
        return get('https://pixlr.com/proxy/?url='+url, headers = {'Accept-Encoding' : 'gzip'}, verify=False).text

    def photopea(url):
        print("Debug: Returning with photopea.")
        return get('https://www.photopea.com/mirror.php?url=' + url, verify=False).text

    def code_beautify(url):
        print("Debug: Returning with code_beautify.")
        headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept':'text/plain, */*; q=0.01',
        'Accept-Encoding':'gzip',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin' : 'https://codebeautify.org',
        'Connection' : 'close'
        }
        return post('https://codebeautify.com/URLService', headers=headers, data='path=' + url, verify=False).text

    response = random.choice([pixlr, photopea, code_beautify])(url)
    return response
