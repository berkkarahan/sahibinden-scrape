# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 18:19:54 2019

@author: karah
"""

from s_scrape.io import IO

l = IO.pickle_load("dumped_listings.pkl")

keys = list(l[0].keys())

import csv

with open('sahibinden_11062019.csv', mode='w', newline='', encoding='utf-8') as f:
    fw = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    fw.writerow(keys)
    
    for itm in l:
        try:
            print("--> Writing car: "+itm['Marka']+" with clsid: "+itm['clsid']+" to csv.")
            values = list(itm.values())
            fw.writerow(values)
        except TypeError:
            continue
