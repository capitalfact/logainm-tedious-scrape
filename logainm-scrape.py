import codecs
import requests
from lxml import etree

base_url = 'http://www.logainm.ie/xml/'

place_name_filename = 'place_name.csv'
place_type_filename = 'place_type.csv'
place_filename = 'place.csv'
place_is_in_filename = 'place_is_in.csv'

place_name = codecs.open(place_name_filename, 'w', "utf-8")
place_type = codecs.open(place_type_filename, 'w', "utf-8")
place = codecs.open(place_filename, 'w', "utf-8")
place_is_in = codecs.open(place_is_in_filename, 'w', "utf-8")

place_name.truncate()
place_type.truncate()
place.truncate()
place_is_in.truncate()

place_name.write("lang_en,lang_ga\n")

parser = etree.XMLParser(encoding='utf-8')

for i in range(10):
	response = requests.get(base_url + str(i), headers = { 'Content-Type':'application/xml'})

	xml = etree.XML(response.content, parser)

	non_existent_place = xml.xpath("//place[@nonexistent='yes']/source")

	if non_existent_place:
		print base_url + str(i) + ": INVALID"
	else:
		print "Processing: " + base_url + str(i)  
		place_names = xml.xpath("//name")
		if len(place_names) != 2:
			print "Too many names."
			break
		en_name = xml.xpath("//name[@lang='en']")[0].get('wording')
		ga_name = xml.xpath("//name[@lang='ga']")[0].get('wording')
		place_name.write(en_name + "," + ga_name + "\n")

place_name.close()
place_type.close()
place.close()
place_is_in.close()	
