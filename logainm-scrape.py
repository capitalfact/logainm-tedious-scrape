import codecs
import requests
from lxml import etree

base_url = 'http://www.logainm.ie/xml/'

place_name_filename = 'place_name.csv'
place_type_filename = 'place_type.csv'
place_filename = 'place.csv'
place_is_in_filename = 'place_is_in.csv'

place_name_csv = codecs.open(place_name_filename, 'w', "utf-8")
place_type_csv = codecs.open(place_type_filename, 'w', "utf-8")
place_csv = codecs.open(place_filename, 'w', "utf-8")
place_is_in_csv = codecs.open(place_is_in_filename, 'w', "utf-8")

place_name_csv.truncate()
place_type_csv.truncate()
place_csv.truncate()
place_is_in_csv.truncate()

#place_name_csv.write("lang_en,lang_ga\n")

parser = etree.XMLParser(encoding='utf-8')

place_types = set() 

place_name_id = 1
place_type_id = 1
place_name_to_id = {}
place_type_to_id = {}

for i in range(10):
	response = requests.get(base_url + str(i), headers = { 'Content-Type':'application/xml'})

	xml = etree.XML(response.content, parser)

	non_existent_place = xml.xpath("//place[@nonexistent='yes']/source")

	if non_existent_place:
		print base_url + str(i) + ": INVALID"
	else:
		print "Processing: " + base_url + str(i)  

		# place_name
		place_names = xml.xpath("//name")
		if len(place_names) != 2:
			print "Too many names."
			break
		en_name = xml.xpath("//name[@lang='en']")[0].get('wording')
		ga_name = xml.xpath("//name[@lang='ga']")[0].get('wording')
		key = en_name + "/" + ga_name
		place_name_to_id[key] = place_name_id
		place_name_csv.write(str(place_name_id) + "," + en_name + "," + ga_name + "\n")
		place_name_id += 1

		# place_type
		place_type = xml.xpath("//type")[0]
		place_type_code = place_type.get('id')
		place_type_name_en = place_type.get('titleEN')
		place_type_name_ga = place_type.get('titleGA')

		if place_type_code not in place_type_to_id:
			place_type_to_id[place_type_code] = place_type_id
			place_types.add(str(place_type_id) + "," + place_type_code + "," + place_type_name_en + "," + place_type_name_ga + "\n")
			place_type_id += 1

for type in place_types:
	place_type_csv.write(type)

place_name_csv.close()
place_type_csv.close()
place_csv.close()
place_is_in_csv.close()	
