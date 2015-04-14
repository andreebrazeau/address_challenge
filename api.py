"""A note on security: were I putting users' actual billing addresses in this app, I'd absolutely 
require OAuth2. Since I could see an OAuth2 implentation taking up half of the time I have to complete
this excercise, I'm making the call to use http only to get geocoords. Since the app theoretically deals 
with users' financial and physical location info, it would be **very important** to use SSL, IMO.

Please see https://developers.google.com/maps/documentation/geocoding/ for more info."""

import os


API_KEY = os.environ.get['GEOCODING_API_KEY']

BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?'

def get_geocoords(address, city, state):
	"""Function should take address, city and state as strings and
	 return a tuple with the latitude and longitude of that address.

	 If none is found, the coordinates of the city and state should be returned."""
