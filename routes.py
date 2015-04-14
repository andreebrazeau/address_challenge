from flask import Flask, render_template, request
import api
import os
import database_things as db


FLASK_SESSION_KEY = os.environ['FLASK_SESSION_KEY']

app = Flask(__name__)
app.secret_key = FLASK_SESSION_KEY


@app.route('/')
def go_home():
	return render_template('addressadder.html')


# Note: for a larger and more complicated app, I'd likely break this 
@app.route('/capture_data', methods=['GET'])
def capture_data():

	db.connect()

	address_to_enter = db.Address()
	# import pdb; pdb.set_trace()
	address.username = request.args.get("username")
	address.name = request.args.get("name")
	address.city_name = request.args.get("city")
	address.state_abbreviation = request.args.get("state")
	address.zipcode = request.args.get("zipcode")

	# Converting the string input to a bool. Here I might ask a business 
	# owner what the preferred default is, but it's not a huge deal since I can set
	# the radio button to be required and force the user to make a choice.
	if request.args.get.is_billing == "true":
		address.is_billing = True
	else:
		address.is_billing = False

	# TODO: Make the API call to get geocoords.
	# Hardcoding geocoords to 200, 200 for testing at the moment. 
	address.latitude = str(200)
	address.longitude = str(200)

	# Add the address object to the ORM database session
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


