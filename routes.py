from flask import Flask, render_template, request
import api
import os
import database_things as db
import db_lookups as dbcheck


FLASK_SESSION_KEY = os.environ['FLASK_SESSION_KEY']

app = Flask(__name__)
app.secret_key = FLASK_SESSION_KEY


@app.route('/')
def go_home():
	return render_template('addressadder.html')


# Note: for a larger and more complicated app, I'd likely move most of this code into a model,
# but since the requirements are fairly focused and straightforward, all the code's here.
@app.route('/capture_data', methods=['GET'])
def capture_data():
	# calling this dbsession to differentiate from a Flask session object
	dbsession = db.connect()
	new_address = db.Address()

	username_str = request.args.get("username")
	username_obj = dbcheck.find_username(username_str, dbsession)

	new_address.username = username_obj
	new_address.name = request.args.get("name")
	new_address.name_secondary = request.args.get("name2")

	city_str = request.args.get("city")
	city_obj = dbcheck.find_city(city_str, dbsession)
	new_address.city_name = city_obj

	state_abbr_str = request.args.get("state")
	state_obj = dbcheck.find_state(state_abbr_str, dbsession)
	new_address.state_abbreviation = state_obj
	
	zipcode_str = request.args.get("zipcode")
	zipcode_obj = dbcheck.find_zipcode(zipcode_str, dbsession)
	new_address.zipcode = zipcode_obj

	# Converting the string input to a bool. Here I might ask a business 
	# owner what the preferred default is, but it's not a huge deal since I can set
	# the radio button to be required and force the user to make a choice.
	if request.args.get("is_billing") == "true":
		new_address.is_billing = True
	else:
		new_address.is_billing = False

	geocoords = api.get_geocoords(new_address)

	new_address.latitude, new_address.longitude = geocoords

	# Add the new_address object to the ORM database session
	dbsession.add(new_address)
	# SQLAlchemy creates an open transaction by default; need to commit the DB transaction.
	dbsession.commit()

	return render_template("confirmation.html")


PORT = int(os.environ.get("PORT", 5000))

if __name__ == '__main__': 
	app.run( 
		debug=True,
		port=PORT,
		host='127.0.0.1',
		ssl_context=('server.crt', 'server.key'))


