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

def find_geocoords(address):
	"""Function should take an address object and return a tuple 
	with the latitude and longitude of that address. If none is found,
	the coordinates of the city and state should be returned."""

	dict_response = call_api(address=address.name, city=address.city_name, state=address.state_abbreviation)

	# Check that we have results before extracting coords:
	if dict_response['status'] == 'OK':
		lat = dict_response['results'][0]['geometry']['location']['lat']
		lon = dict_response['results'][0]['geometry']['location']['lng']
		coords = (lat, lon)
		return coords

	# If no results, call API again for just city and state
	elif dict_response['status'] == 'ZERO_RESULTS':
		dict_response = call_api(city=address.city_name, state=address.state_abbreviation)
	elif:
		dict_response = call_api(state=address.state)

	else:
		# In the unlikely event there aren't geocoords for the state, return hardcoded coords
		# for USA. In production, I might instrument this to notify someone that the
		# geocoord API might be down or have another issue requiring an engineer's attention.
		return (0,0)


def call_api(**kwargs):
	"""Function to fetch geocoordinates for any combination of parameters accepted
	by the Google Geocoding API."""

	# Put args in the right order for the API:



	encoded_parameters = quote_plus()
	api_request = BASE_URL + "address=" + encoded_parameters + "&key=" + API_KEY

	response = requests.get(api_request)
	# response_string = str(response.content)
	dict_response = json.loads(response.content)
	print dict_response

	return response_as_dict



def main():
	pass


if __name__ == '__main__':
	main()
