# -*- coding: utf-8 -*-
"""Logainm Scraper"""

import requests
from logainmdb import persist
from logainmparser import LogainmParser
from socket import error as SocketError

# for utf8 print to console
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

EN = 'en'
GA = 'ga'
BASE_URL = 'http://www.logainm.ie/xml/'

FAILED_LOG = open('output/failed.log', 'w+')

class LogainmScraper:
    def __init__(self, fromrange, torange):
        self.fromrange = fromrange
        self.torange = torange

    def scrape(self):

        for i in range(self.fromrange, self.torange):

            try:
                response = requests.get(BASE_URL + str(i), headers={'Content-Type': 'application/xml'})
            except SocketError as e:
                FAILED_LOG.write(str(i))

            if response is None or response.status_code != 200:
                continue

            logainmparser = LogainmParser(response.content)

            if not logainmparser.placeexists():
                print BASE_URL + str(i) + ": INVALID"
            else:
                place = logainmparser.getplace()
                persist(place)

                print str(i) + ": " + str(place)

                # is in relationships
                # is_ins = logainmparser.getallelements("isIn")
                # for is_in in is_ins:
                #    belongs_to = is_in.get('placeID')
                #    PLACE_IS_INS_CSV.writerow((str(i), belongs_to))

