from flask import Flask, render_template
import api


@app.route('/capture_data', methods=['GET', 'POST'])
def capture_data():
	# First, create new address object, and assign its attributes according to form parameters. 

	# Check if the username exists in the DB already.


	address.username = request.form("username")
	address.name = request.form("name")
	address.city = request.form("city")
	address.state = request.form("state")
	address.zipcode = request.form("zipcode")

	# Converting the string input to a bool. Here I might ask a business 
	# owner what the preferred default is, but it's not a huge deal since I can set
	# the radio button to be required and force the user to make a choice.
	if form.is_billing == "true":
		address.is_billing = True
	else:
		address.is_billing = False

	# TODO: Make the API call to get geocoords
	# Write the geocoords to DB
	address.latitude = lat_from_api
	address.longitude = lon_from_api

	return render_template("confirmation.html")


