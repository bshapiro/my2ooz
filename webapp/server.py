#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ

from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine

app = flask.Flask(__name__)
app.debug = True
engine = create_engine('mysql://my2ooz:w3rnid@/my200z', convert_unicode=True)
db = SQLAlchemy(app)


@app.route("/")
def test_all_calls():
    connection = engine.connect()
    # TESTS FOR WEEK INFO
    all_info = get_all_info(connection, 0)
    week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    week_genres = []
    for day in week:
        week_genres.append(get_day_info(connection, day, 0))

    all_info_string = "all info for venue 0: " + all_info
    week_genres_string = ""
    for day in week:
        week_genres_string += day + ": " + week_genres[week.index(day)]
        
    venue_info = get_venue_info(connection, 0)
    
    final_string = all_info_string + week_genres_string + venue_info 
    
    
    # END TESTS
    
    # TESTS FOR VENUE INFO
    # END TESTS

    connection.close()
    return final_string

def get_all_info(connection, venue_id):
    query = 'select * from venue_table where venue_id = ' + str(venue_id)
    data = connection.execute(query)
    return stringerize(data)


def get_day_info(connection, day, venue_id):
    query = 'select ' + day + ' from venue_table where venue_id = ' + str(venue_id)
    data = connection.execute(query)
    return stringerize(data)

def get_venue_info(connection, venue_id):
    query = 'select manager_name, food_drink from venue_table where venue_id = ' + str(venue_id)
    data = connection.execute(query)
    return stringerize(data)
    
def stringerize(sql_object):
    string = ""
    for row in sql_object:
	string += str(row) + "</br>"
    return string

if __name__ == "__main__":
    app.run(port=61004)
