#Delay constants for reading URLs with uniform random wait time
LOWER_DELAY = 0.5
UPPER_DELAY = 0.8

class Scraper():
    def __init__(self,url=""):
        self._link = url

    @property
    def link(self):
        return self._link
