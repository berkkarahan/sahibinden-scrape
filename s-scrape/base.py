
class Scraper():
    def __init__(self,url):
        self._link = url

    @property
    def link(self):
        return self._link
