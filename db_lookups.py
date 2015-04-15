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
		dbsession.commit()
	else:
		# Assign the existing user object to the variable
		username_object = first_row

	return username_object








