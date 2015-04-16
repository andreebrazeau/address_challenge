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

	session = db.connect()
	new_address = db.Address()

	username_str = request.args.get("username")
	username_obj = dbcheck.find_username(username_str, session)
	new_address.username = username_obj
	new_address.name = request.args.get("name")

	city_str = request.args.get("city")
	# FIXME: for this function call to find_city(), I get a SQLAlchemy error returned stating that 
	# 'AttributeError: Could not locate column in row for column '_sa_instance_state''.
	# However, this error is thrown at line 29 of this file. Yet when I *don't* make the function call
	# to find_city() here, line 29 seems to succeed.
	# 
	# Clearly the issue has to do with how the SQLAlchemy ORM behaves, but unfortunately I've run out of
	# time to familiarize myself with this fairly complicated tool. 

	city_obj = dbcheck.find_city(city_str, session)
	new_address.city_name = city_obj


	new_address.state_abbreviation = request.args.get("state")
	new_address.zipcode = request.args.get("zipcode")

	# Converting the string input to a bool. Here I might ask a business 
	# owner what the preferred default is, but it's not a huge deal since I can set
	# the radio button to be required and force the user to make a choice.
	if request.args.get.is_billing == "true":
		new_address.is_billing = True
	else:
		new_address.is_billing = False

	# TODO: Make the API call to get geocoords.
	# Hardcoding geocoords to 200, 200 for testing at the moment. 
	new_address.latitude = str(200)
	new_address.longitude = str(200)

	# Add the new_address object to the ORM database session
	db.add(new_address)
	# SQLAlchemy creates an open transaction by default; need to commit the DB transaction.
	db.commit()

	return render_template("confirmation.html")


PORT = int(os.environ.get("PORT", 5000))

if __name__ == '__main__': 
	app.run( 
		debug=True,
		port=PORT,
		host='127.0.0.1')


