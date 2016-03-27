"""Logainm Scraper"""

import codecs
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

PLACE_TYPES_SET = set()

PLACE_ID = 1
PLACE_NAME_ID = 1
PLACE_TYPE_ID = 1
PLACE_NAME_TO_ID = {}
PLACE_TYPE_TO_ID = {}

for i in range(248,249):

    try:
        response = requests.get(BASE_URL + str(i), headers={'Content-Type': 'application/xml'})
    except SocketError as e:
        FAILED_LOG.write(str(i))

    if not response:
        continue

    place = LogainmParser(response)

    if not place.exists():
        print BASE_URL + str(i) + ": INVALID"
    else:
        print "Processing: " + BASE_URL + str(i)

        # place_name
        en_name = place.get_main_name(EN)
        ga_name = place.get_main_name(GA)

        if en_name == '':
            print "No name in English\n"
        elif ga_name == '':
            print "Gan ainm as Gaeilge\n"

        key = "%s/%s", en_name, ga_name
        PLACE_NAME_TO_ID[key] = PLACE_NAME_ID
        PLACE_NAMES_CSV.writerow((str(PLACE_NAME_ID), en_name, ga_name))
        PLACE_NAME_ID += 1

        # place_type
        type_element = place.getelement('type')

        place_type_code = type_element.get('id')
        place_type_name_en = type_element.get('titleEN')
        place_type_name_ga = type_element.get('titleGA')

        if place_type_code not in PLACE_TYPE_TO_ID:
            PLACE_TYPE_TO_ID[place_type_code] = PLACE_TYPE_ID
            PLACE_TYPES_SET.add((str(PLACE_TYPE_ID), place_type_code, place_type_name_en, place_type_name_ga))
            PLACE_TYPE_ID += 1

        # place
        logainm_id = i
        name_id = PLACE_NAME_TO_ID["%s/%s", en_name, ga_name]
        type_id = PLACE_TYPE_TO_ID[place_type_code]
        geo = place.getelement('geo')
        lon = place.getelementattribute(geo, 'lon')
        lat = place.getelementattribute(geo, 'lat')
        geo_accurate = 0
        if place.getelementattribute(geo, 'isAccurate') == 'yes':
            geo_accurate = 1

        PLACES_CSV.writerow((str(PLACE_ID), str(logainm_id), str(name_id), str(type_id), lon, lat, str(geo_accurate)))

        PLACE_ID += 1

        # is in relationships

        is_ins = place.getallelements("isIn")
        for is_in in is_ins:
            belongs_to = is_in.get('placeID')
            PLACE_IS_INS_CSV.writerow((str(i), belongs_to))

for place_type in PLACE_TYPES_SET:
    PLACE_TYPES_CSV.writerow(place_type)

PLACE_NAMES_FH.close()
PLACE_TYPES_FH.close()
PLACES_FH.close()
PLACE_IS_INS_FH.close()
