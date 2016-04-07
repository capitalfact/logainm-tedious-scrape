"""Logainm data base scraping and parsing"""
from lxml import etree
from logainmdb import Place, PlaceName, PlaceType
import csv

PARSER = etree.XMLParser(encoding='utf-8')
REL_FH = open('output/relationships.csv', 'w+')
REL_CSV = csv.writer(REL_FH)

class LogainmParser:
    def __init__(self, response):
        self.responsexml = etree.XML(response, PARSER)

    def getplace(self):
        # get first place for now
        placeobj = self.getallelements('place')[0]

        logainm_id = placeobj.get('id')
        place_name = self.getplacename()
        place_type = self.getplacetype()

        geos = self.getallelements('geo')
        lon = None
        lat = None
        geo_accurate = False
        if geos is not None and len(geos) > 0:
            lon = geos[0].get('lon')
            lat = geos[0].get('lat')
            if geos[0].get('isAccurate') == 'yes':
                geo_accurate = True

        self.writeparents(logainm_id)

        return Place(logainm_id, place_name, place_type, lon, lat, geo_accurate)

    def getplacename(self):
        wording_en = ''
        wording_ga = ''
        for name in self.getallelements("name"):
            if name.get('isMain') == 'yes':
                wording = name.get('wording')
                lang = name.get('lang')
                if lang == 'en':
                    wording_en = wording
                elif lang == 'ga':
                    wording_ga = wording
        return PlaceName(wording_en, wording_ga)

    def getplacetype(self):
        code = ''
        name_en = ''
        name_ga = ''
        typeelems = self.getallelements('type')
        if typeelems is not None and len(typeelems) > 0:
            code = typeelems[0].get('id')
            name_en = typeelems[0].get('titleEN')
            name_ga = typeelems[0].get('titleGA')
        return PlaceType(code, name_en, name_ga)

    def writeparents(self, logainm_id):
        for parent in self.getrelationships():
            REL_CSV.writerow([parent, logainm_id])

    def getrelationships(self):
        relations = [] # logainm_id mapping
        for relation in self.getallelements("isIn"):
            relations.append(relation.get('placeID'))
        return relations

    def getelement(self, element):
        elements = self.responsexml.xpath('//' + element)
        if elements and len(elements) > 0:
            return self.responsexml.xpath('//' + element)[0]

    def getelementattribute(self, element, attr):
        if element is not None:
            return element.get(attr)
        else:
            return ''

    def getallelements(self, element):
        return self.responsexml.xpath('//' + element)

    def placeexists(self):
        places = self.getallelements('place')
        if places is not None and len(places) > 0:
            nonexistent = places[0].get('nonexistent')
            if nonexistent == 'yes':
                return False
        return True
