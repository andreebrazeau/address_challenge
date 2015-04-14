"""A note on naming conventions in this module: I use plurals for table names, 
implying that there is more than one record in a table. I use singular terms for class names,
following Python convention."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


ENGINE = None
Session = None

DATABASE_URL = 'postgresql://localhost:5432/BioRetro'


def make_tables():
	""" This function only needs to be called when making a change to a table's schema."""
	ENGINE = create_engine(DATABASE_URL, echo=False)
	Base.metadata.create_all(ENGINE)


class Address(Base):
	"""Retaining the unique component of the address in the address table, using additional tables 
	for city, state et cetera to accommodate later expansion into other markets as need be."""
	
	__tablename__ = "Addresses"

	id = Column(Integer, primary_key=True)
	name = Column(, not_null=True)
	user_id = Column(Integer, not_null)
	is_billing = Column(Boolean, not_null=True)
	city_id = Column(Integer, not_null=True)
	state_id = Column(String, not_null=True)
	zipcode_id = Column(String, not_null=True)
	latitude = Column(String, not_null=True)
	longitude = Column(String, not_null=True)


class User(Base):
	
	__tablename__ = "Users"

	id = Column(Integer, primary_key=True)
	username = Column(String, not_null=True)


class City(Base):

	__tablename__ = "Cities"	

	id = Column(Integer, primary_key=True)
	city_name = Column(String, primary_key=True)


class State(Base):
	
	__tablename__ = "States"

	id = Column(Integer, primary_key=True)
	state_abbreviation = Column(String, length=2, not_null=True)


class Zipcode(Base):
	
	__tablename__ = "Zipcodes"
	# Making the zipcode a string since I'll never need to use it for artithmetic purposes, so
	# this is easier for building an API request with.
	id = Column(Integer, primary_key=True)
	zipcode = Column(String, not_null=True)


def connect():

	global ENGINE
	global Session
	
	ENGINE = create_engine(DATABASE_URL, echo=False)
	Session = sessionmaker(bind=ENGINE, autocommit=False, autoflush=False)

	return Session()


# make_tables()
