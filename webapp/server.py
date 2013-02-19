#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)

from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine


app = flask.Flask(__name__)
app.debug = True

login_manager = LoginManager()

engine = create_engine('mysql://my2ooz:w3rnid@/my200z', convert_unicode=True)
db = SQLAlchemy(app)


@app.route("/")
def test_all_calls():
    connection = engine.connect()
    
    # BEGIN TESTS
    all_info = stringify(get_all_info(connection))
    week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    week_genres = []
    for day in week:
        week_genres.append(stringify(get_day_info_by_venue_id(connection, day, 0)))

    all_info_string = "all info:  " + all_info
    week_genres_string = ""
    for day in week:
        week_genres_string += day + ": " + week_genres[week.index(day)]
        
    venue_info = 'venue info for existing login: ' + stringify(get_venue_info_by_login(connection, 'login'))
    venue_info_2 = 'venue info for non-existent login: ' + str(get_venue_info_by_login(connection, 'admin'))
    
    final_string = all_info_string + week_genres_string + venue_info + venue_info_2
    # END TESTS

    connection.close()
    return final_string

def get_all_info(connection):
    query = 'select * from venue_table'
    data = connection.execute(query)
    return data


def get_day_info_by_venue_id(connection, day, venue_id):
    query = 'select ' + day + ' from venue_table where venue_id = ' + str(venue_id)
    data = connection.execute(query)
    return data

def get_venue_info_by_login(connection, login):
    query = 'select * from venue_table where login = ' + str(login)
    try:
	data = connection.execute(query)
    except Exception:
	return None
    return data
    

def stringify(sql_object):
    string = ""
    for row in sql_object:
	string += str(row) + "</br>"
    return string

class User():

    def __init__(self, venue_info, active=True):
	if venue_info != None:
	    self.name = venue_info['manager_name']
 	    self.venue_id = venue_info['venue_id']
	    self.location_name = venue_info['location_name']
	    self.venue_type = venue_info['venue_type']
	    self.login = venue_info['login']
	    self.password = venue_info['password']
	    self.monday = venue_info['monday']
	    self.tuesday = venue_info['tuesday']
	    self.wednesday = venue_info['wednesday']
	    self.thursday = venue_info['thursday']
	    self.friday = venue_info['friday']
	    self.saturday = venue_info['saturday']
	    self.sunday = venue_info['sunday']
	    self.food_drink = venue_info['food_drink']
	    self.is_authenticated = True
        else:
	    self.is_authenticated = False
	self.active = active
    
    def is_active(self):
        return self.active
    
    def is_authenticated(self):
	return self.is_authenticated

    def is_anonymous(self):
	return False

    def get_id(self):
	return unicode(self.venue_id)

if __name__ == "__main__":
    app.run(port=61004)
