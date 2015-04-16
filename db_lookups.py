"""A note on keeping code DRY: here I would optimally create one function that can dynamically 
check different DB tables depending on which parameters are passed. However given my knowledge of 
SQLAlchemy is still developing, Wednesday's deadline, and that my code is working for find_username, 
I'm going to make a new function for each class that I'm checking the DB for. 

This makes it easier for me to write straight SQL when checking for existing records, 
which I'm much better at than ORMs anyway. :)"""


import database_things as db

def find_username(username, dbsession):
	"""Checks the db if there is a username matching the passed parameter already and returns the username object. 
	If there isn't, it writes the username to the db and returns the new username object."""

	result = dbsession.execute('SELECT * from "Users" where username = :name LIMIT 1', {'name': username})
	first_row = result.first()

	# Need to extract the object from the ORM result proxy.
	if first_row is None:
		# Create a new instance of user
		username_object = db.User(username)
		dbsession.add(username_object)
		dbsession.flush()
		dbsession.commit()
	else:
		# Assign the existing user object to the variable
		username_object = first_row

	return username_object


def find_city(city, dbsession):
	"""Checks the db if there is a city matching the passed parameter already and returns the city object. 
	If there isn't, it writes the city to the db and returns the new city object.

	FIXME"""

	# Since we're creating the FK relation based on ID, and hence the casing has no bearing on 
	# whether the city record associates with the address, I'm upcasing the city to prevent dupes.
	city = city.uppercase()

	city_result = dbsession.execute('SELECT * from "Cities" where city_name = :name LIMIT 1', {'name': city})
	first_city_row = city_result.first()

	# Need to extract the object from the ORM result proxy.
	if first_row is None:
		# Create a new instance of city
		city_object = db.City(city)
		dbsession.add(city_object)
		dbsession.flush()
		dbsession.commit()
	else:
		# Assign the existing user object to the variable
		city_object = first_city_row

	return city_object




