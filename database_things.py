"""A note on naming conventions in this module: I use plurals for table names, 
implying that there is more than one record in a table. I use singular terms for class names,
following Python convention."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
import psycopg2


DATABASE_URL = 'postgresql://localhost:5432/address_challenge'

ENGINE = None
session = None

Base = declarative_base()
# Base.query = session.query_property()


def make_tables():
	""" This function only needs to be called when making a change to a table's schema."""
	ENGINE = create_engine(DATABASE_URL, echo=False)
	Base.metadata.create_all(ENGINE)


class Address(Base):
    """Retaining the unique component of the address in the address table, using additional tables
    for city, state et cetera to accommodate later expansion into other markets as need be."""

    __tablename__ = "Addresses"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    name_secondary = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    type = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey("Cities.id"), nullable=False)
    state_id = Column(Integer, ForeignKey("States.id"), nullable=False)
    zipcode_id = Column(Integer, ForeignKey("Zipcodes.id"), nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)

    username = relationship("User", backref=backref("addresses"))
    city_name = relationship("City", backref=backref("addresses"))
    state_abbreviation = relationship("State", backref=backref("addresses"))
    zipcode = relationship("Zipcode", backref=backref("addresses")) 

    def __repr__(self):
        return "<Address object %s>" % self.name


class User(Base):
	
	__tablename__ = "Users"

	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False)

	def __init__(self, username):
		self.username = username

	def __repr__(self):
		return "<Username object s%>" % self.username


class City(Base):  # Why creating a separate table for the city?

	__tablename__ = "Cities"	

	id = Column(Integer, primary_key=True)
	city_name = Column(String, primary_key=False)

	def __init__(self, city_name):
		self.city_name = city_name

	def __repr__(self):
		return "<City object s%>" % self.city_name


class State(Base):

	__tablename__ = "States"

	id = Column(Integer, primary_key=True)
	state_abbreviation = Column(String(2), nullable=False)

	def __repr__(self):
		return "<State object %s>" % self.state_abbreviation


class Zipcode(Base):

	__tablename__ = "Zipcodes"
	# Making the zipcode a string since I'll never need to use it for artithmetic purposes, so
	# this is easier for building an API request with.
	id = Column(Integer, primary_key=True)
	zipcode = Column(String, nullable=False)

	def __init__(self, zipcode):
		self.zipcode = zipcode

	def __repr__(self):
		return "<Zipcode object s%>" % self.zipcode	


def connect():

	global ENGINE
	global Session
	
	ENGINE = create_engine(DATABASE_URL, echo=False)
	Session = sessionmaker(bind=ENGINE, autocommit=False, autoflush=False)

	return Session()


# make_tables()
