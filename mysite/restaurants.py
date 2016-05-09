import xml.etree.ElementTree as ET
import urllib2

def find_rest(place):

	place = place.replace(" ", "+")
	place = place.replace(",", "+")
	hotels = []

	loc = "https://maps.googleapis.com/maps/api/geocode/xml?address=" + place +"&key=AIzaSyBaLkqyn64UMjeCzNd2BNWIide3EhnSuL8"

	page = urllib2.urlopen(loc)

	tree = ET.parse(page)
	root = tree.getroot()

	for neighbor in root.iter('location'):
		lat = neighbor[0].text 
		lon = neighbor[1].text


	rest_path = "https://maps.googleapis.com/maps/api/place/nearbysearch/xml?location="+ lat + "," + lon + "&radius=10000&type=restaurant&key=AIzaSyBaLkqyn64UMjeCzNd2BNWIide3EhnSuL8"

	restaurants = urllib2.urlopen(rest_path)

	tree = ET.parse(restaurants)
	root = tree.getroot()

	for rests in root.findall('result'):
		name = rests.find('name').text
		hotels.append(name)
		vicinity = rests.find('vicinity').text
		hotels.append(vicinity)
		if rests.find('rating') is not None:
			rating = rests.find('rating').text
			hotels.append("Rating:" + str(rating))
		hotels.append("\n")
	return hotels


