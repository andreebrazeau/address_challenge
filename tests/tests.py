import nose
import db_lookups as lookup
import database_things as db
# Possible options for db strategy:
	# -Run tests against a test DB
	# -In setup of ,delete the user with my test username -> went this route in the interest of time, seems
	# unnecessarily time consuming to spin up a new test DB for a smallish project like this one.
	# -Create a global setup function that drops and recreates the applicable tables before each suite run. 
	# *this is the option I would have preferred,* but didn't worry about in the interest of time (figuring
		# out the ORM stuff kind of took a while.)

# Setup
# Action
# Assert


def test_find_username():
	# Setup by deleting the username from previous test runs
	dbsession = db.connect()
	dbsession.execute('delete from "Users" where username = \'amanda_new\'')
	
	# call the function under test
	lookup.find_username("amanda_new", dbsession)

	# assert the info got written to the DB
	result = dbsession.execute('select * from "Users" where username = \'amanda_new\'')
	username = result.first().username

	assert username == 'amanda_new'


# Interesting ORM note! This one helped me catch a bug in the "else" statement of the find_username() function.
# Turns out that once my code fetches a record/ORM class object from a ResultProxy object, it's
# physically removed from the object and the ResultProxy is closed. So the fix was to store the 
# record I fectch from the ResultProxy object into a variable so I can make additional
# logic checks against that object after the connection has closed. 

# further note 5/4/15: I changed the code to use the session.query() function instead of session.execute(),
# which obviates the need for the ResultProxy object. So the above is moot but still a good thing
# to know when executing raw SQL through an ORM.
def test_username_exists():

	# Setup by deleting the username from previous test runs
	dbsession = db.connect()
	result = dbsession.execute('select * from "Users" where username = \'amg\'')
	num_records = result.rowcount
	assert num_records == 1

	# call the function under test
	username_object = lookup.find_username("amg", dbsession)

	assert username_object.username == 'amg'
	result = dbsession.execute('select * from "Users" where username = \'amg\'')
	assert result.rowcount == 1


def test_api_call():
	pass




