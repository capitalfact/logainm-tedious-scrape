import requests
from lxml import etree

base_url = 'http://www.logainm.ie/xml/'

parser = etree.XMLParser(encoding='utf-8')

for i in range(10):
	response = requests.get(base_url + str(i), headers = { 'Content-Type':'application/xml'})

	xml = etree.XML(response.content, parser)

	non_existent_place = xml.xpath("//place[@nonexistent='yes']/source")

	if non_existent_place:
		print base_url + str(i) + ": INVALID"
	else:
		print base_url + str(i) + ": VALID" 
		
