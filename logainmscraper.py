"""Logainm Scraper"""

import requests
import unicodecsv as csv
from logainmparser import LogainmParser
from socket import error as SocketError

EN = 'en'
GA = 'ga'
BASE_URL = 'http://www.logainm.ie/xml/'

PLACE_NAMES_FH = open('output/place_name.csv', 'w+')
PLACE_TYPES_FH = open('output/place_type.csv', 'w+')
PLACES_FH = open('output/place.csv', 'w+')
PLACE_IS_INS_FH = open('output/place_is_in.csv', 'w+')
FAILED_LOG = open('output/failed.log', 'w+')

PLACE_NAMES_CSV = csv.writer(PLACE_NAMES_FH, encoding='utf-8')
PLACE_TYPES_CSV = csv.writer(PLACE_TYPES_FH, encoding='utf-8')
PLACES_CSV = csv.writer(PLACES_FH, encoding='utf-8')
PLACE_IS_INS_CSV = csv.writer(PLACE_IS_INS_FH, encoding='utf-8')


class LogainmScraper:
    def __init__(self, fromrange, torange):
        self.fromrange = fromrange
        self.torange = torange

    def scrape(self):

        # id counters
        place_id = 1
        place_name_id = 1
        place_type_id = 1

        # relationship maps
        place_name_id_map = {}
        place_type_id_map = {}

        place_types_set = set()

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
                print "Processing: " + BASE_URL + str(i)

                place = logainmparser.getplace()

                # place_name
                place_name = place.place_name
                PLACE_NAMES_CSV.writerow((str(place_name.id), place_name.getname('en'), place_name.getname('ga')))
                place_name_id += 1

                # place_type
                place_type = place.place_type
                place_type_code = place_type.code

                if place_type_code not in place_type_id_map:
                    place_type_id_map[place_type_code] = place_type_id
                    place_types_set.add((str(place_type.id), place_type.code, place_type.desc_en, place_type.desc_ga))
                    place_type_id += 1

                # place
                PLACES_CSV.writerow(
                    (str(place.id),
                     str(place.logainm_id),
                     str(place.place_name_id),
                     str(place.place_type_id),
                     str(place.longitude),
                     str(place.latitude),
                     str(place.geo_accurate)))
                place_id += 1

                # is in relationships
                #is_ins = logainmparser.getallelements("isIn")
                #for is_in in is_ins:
                #    belongs_to = is_in.get('placeID')
                #    PLACE_IS_INS_CSV.writerow((str(i), belongs_to))

        for place_type in place_types_set:
            PLACE_TYPES_CSV.writerow(place_type)

        PLACE_NAMES_FH.close()
        PLACE_TYPES_FH.close()
        PLACES_FH.close()
        PLACE_IS_INS_FH.close()
