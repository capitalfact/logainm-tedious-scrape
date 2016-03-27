#!/usr/bin/env python
"""Logainm Scraper"""

import codecs
import requests
from lxml import etree

BASE_URL = 'http://www.logainm.ie/xml/'

PLACE_NAME_FILENAME = 'output/place_name.csv'
PLACE_TYPE_FILENAME = 'output/place_type.csv'
PLACE_FILENAME = 'output/place.csv'
PLACE_IS_IN_FILENAME = 'output/place_is_in.csv'

PLACE_NAME_CSV = codecs.open(PLACE_NAME_FILENAME, 'w', "utf-8")
PLACE_TYPE_CSV = codecs.open(PLACE_TYPE_FILENAME, 'w', "utf-8")
PLACE_CSV = codecs.open(PLACE_FILENAME, 'w', "utf-8")
PLACE_IS_IN_CSV = codecs.open(PLACE_IS_IN_FILENAME, 'w', "utf-8")

PLACE_NAME_CSV.truncate()
PLACE_TYPE_CSV.truncate()
PLACE_CSV.truncate()
PLACE_IS_IN_CSV.truncate()

PARSER = etree.XMLParser(encoding='utf-8')

PLACE_TYPES = set()

PLACE_ID = 1
PLACE_NAME_ID = 1
PLACE_TYPE_ID = 1
PLACE_NAME_TO_ID = {}
PLACE_TYPE_TO_ID = {}

for i in range(2):
    response = requests.get(BASE_URL + str(i), headers={'Content-Type': 'application/xml'})

    xml = etree.XML(response.content, PARSER)

    non_existent_place = xml.xpath("//place[@nonexistent='yes']/source")

    if non_existent_place:
        print BASE_URL + str(i) + ": INVALID"
    else:
        print "Processing: " + BASE_URL + str(i)

        # place_name
        en_name = ""
        ga_name = ""
        en_names = xml.xpath("//name[@lang='en']")
        for en in en_names:
            if en.get('isMain') == "yes":
                en_name = en.get('wording')
        ga_names = xml.xpath("//name[@lang='ga']")
        for ga in ga_names:
            if ga.get('isMain') == "yes":
                ga_name = ga.get('wording')
        if en_name == "" or ga_name == "":
            print "Problem with names"

        key = en_name + "/" + ga_name
        PLACE_NAME_TO_ID[key] = PLACE_NAME_ID
        PLACE_NAME_CSV.write(str(PLACE_NAME_ID) + "," + en_name + "," + ga_name + "\n")
        PLACE_NAME_ID += 1

        # place_type
        place_type_obj = xml.xpath("//type")[0]
        place_type_code = place_type_obj.get('id')
        place_type_name_en = place_type_obj.get('titleEN')
        place_type_name_ga = place_type_obj.get('titleGA')

        if place_type_code not in PLACE_TYPE_TO_ID:
            PLACE_TYPE_TO_ID[place_type_code] = PLACE_TYPE_ID
            PLACE_TYPES.add(
                str(PLACE_TYPE_ID) + ","
                + place_type_code + ","
                + place_type_name_en
                + "," + place_type_name_ga
                + "\n")
            PLACE_TYPE_ID += 1

        # place
        logainm_id = i
        name_id = PLACE_NAME_TO_ID[en_name + "/" + ga_name]
        type_id = PLACE_TYPE_TO_ID[place_type_code]
        geos = xml.xpath("//geo")
        lon = ""
        lat = ""
        geo_accurate = 0
        if len(geos) > 0:
            geo = xml.xpath("//geo")[0]
            lon = geo.get('lon')
            lat = geo.get('lat')
            if geo.get('isAccurate') == "yes":
                geo_accurate = 1

        PLACE_CSV.write(str(PLACE_ID) + "," + str(logainm_id) + "," + str(name_id) + "," + str(
            type_id) + "," + lon + "," + lat + "," + str(geo_accurate) + "\n")
        PLACE_ID += 1

        # is in relationships
        is_ins = xml.xpath("//isIn")
        for is_in in is_ins:
            belongs_to = is_in.get('placeID')
            PLACE_IS_IN_CSV.write(str(i) + "," + belongs_to + "\n")

for place_type in PLACE_TYPES:
    PLACE_TYPE_CSV.write(place_type)

PLACE_NAME_CSV.close()
PLACE_TYPE_CSV.close()
PLACE_CSV.close()
PLACE_IS_IN_CSV.close()
