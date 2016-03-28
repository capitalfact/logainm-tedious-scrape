"""Logainm data base scraping and parsing"""
from lxml import etree

PARSER = etree.XMLParser(encoding='utf-8')


class LogainmParser:
    def __init__(self, response):
        self.responsexml = etree.XML(response, PARSER)

    def getplace(self):
        # return first place for now
        return self.responsexml.xpath("//place")[0]

    def getelement(self, element):
        elements = self.responsexml.xpath("//" + element)
        if elements and len(elements) > 0:
            return self.responsexml.xpath("//" + element)[0]

    def getelementattribute(self, element, attr):
        if element is not None:
            return element.get(attr)
        else:
            return ''

    def getallelements(self, element):
        return self.responsexml.xpath("//" + element)

    def exists(self):
        exists = self.getplace().get('nonexistent')
        if exists == 'yes':
            return False
        else:
            return True

    def get_main_name(self, lang):
        for name in self.responsexml.xpath("//name[@lang='" + lang + "']"):
            if name.get('isMain') == 'yes':
                wording = name.get('wording')
                if not wording:
                    wording = ''
                return wording
        return ''
