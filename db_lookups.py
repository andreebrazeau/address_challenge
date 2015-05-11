"""A note on keeping code DRY: here I would optimally create one function that can dynamically 
check different DB tables depending on which parameters are passed. For the sake of speed I'm not 
doing that here since I won't always need to check if the record is in the DB before returning the 
related object, e.g. in the case of getting a state object from the DB to create a relationship 
between the new address and the state.

Also, this code assumes the front end would be checking input for formatting, e.g. making sure
a zipcode is a 5 digit string. The ORM layer provides protection from SQL injection so there isn't 
any manual validation in that regard."""


import database_things as db

def find_username(username, dbsession):
    """Checks the db if there is a username matching the passed parameter already and returns the username object. 
    If there isn't, it writes the username to the db and returns the new username object."""

    result = dbsession.query(db.User).filter_by(username=username).first()

    # Need to extract the object from the ORM result proxy.
    if result is None:
        # Create a new instance of user
        username_object = db.User(username)
        dbsession.add(username_object)
        return username_object
    else:
        # Assign the existing user object to the variable
        return result


def find_city(city, dbsession):
    """Checks the db if there is a city matching the passed parameter already and returns the city object. 
    If there isn't, it writes the city to the db and returns the new city object."""

    # Since we're creating the FK relation based on ID, and hence the casing has no bearing on 
    # whether the city record associates with the address, I'm upcasing the city to prevent dupes.
    city = str(city)
    city = city.upper()

    result = dbsession.query(db.City).filter_by(city_name=city).first()

    if result is None:
        # Create a new instance of city
        city_object = db.City(city)
        # I'm adding the city without committing the transaction since it would also
        # commit the address insert transaction that's still open in routes.py.
        dbsession.add(city_object)
        return city_object
    else:
        # Assign the existing user object to the variable
        return result


def find_state(state, dbsession):
    """Fetches a state object by state abbreviation and returns it.
    Assumes that the caller gives it the abbreviation formatted like this: CA

    It doesn't check if the state is present first since the state menu is a dropdown
    so the user cannot submit an invalid state selection."""

    return dbsession.query(db.State).filter_by(state_abbreviation=state).first()


def find_zipcode(zipcode, dbsession):

    result = dbsession.query(db.Zipcode).filter_by(zipcode=zipcode).first()

    if result is None:
        # Create a new instance of zipcode
        zipcode_obj = db.Zipcode(zipcode)
        # I'm adding the city without committing the transaction since it would also
        # commit the address insert transaction that's still open in routes.py.
        dbsession.add(zipcode_obj)
        return zipcode_obj
    else:
        # Assign the existing user object to the variable
        return result

