"""A note on security: were I putting users' actual billing addresses in this app, I'd absolutely 
require OAuth2. Since I could see an OAuth2 implentation taking up half of the time I have to complete
this excercise, I'm making the call to use http only to get geocoords. Since the app theoretically deals 
with users' financial and physical location info, it would be **very important** to use a secured 
connection, IMO.

Please see https://developers.google.com/maps/documentation/geocoding/ for more info."""

import os
import requests
import json
from urllib import quote_plus

API_KEY = os.environ['GEOCODING_API_KEY']

BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'

def get_geocoords(address, city, state):
	"""Function should take API parameters as strings and return a tuple 
	with the latitude and longitude of that address. If none is found,
	the coordinates of the city and state should be returned."""

	encoded_parameters = quote_plus(address + city + state)
	api_request = BASE_URL + "address=" + encoded_parameters + "&key=" + API_KEY

	response = requests.get(api_request)
	# response_string = str(response.content)
	dict_response = json.loads(response.content)

	try:
		lat = dict_response['results'][0]['geometry']['location']['lat']
		lon = dict_response['results'][0]['geometry']['location']['lng']
		coords = (lat, lon)	
		if coords not None:
			# Check that we have coordinates
			return coords
		else:
			return (0,0)
			# # Get the geocoords for the city
			# params = quote_plus("address=" + city + state "&key=" + API_KEY)
			# second_request = BASE_URL + params

	except:
		return (0 ,0)

	# print coords
	# return coords


def main():
	pass


if __name__ == '__main__':
	main()
