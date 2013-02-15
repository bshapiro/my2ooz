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

    all_info = get_all_info(connection, 0)
    week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    week_genres = []
    for day in week:
        week_genres.append(get_day_info(connection, day, 0))

    connection.close()

    all_info_string = "all info for venue 0: " + all_info
    week_genres_string = ""
    for day in week:
        week_genres_string += day + ": " + week_genres[week.index(day)]
    final_string = all_info_string + week_genres_string

    return final_string


def get_all_info(connection, venue_id):
    data = connection.execute('select * from venue_table where venue_id = ' + str(venue_id))
    string = ""
    for row in data:
        string += str(row) + "</br>"
    return string


def get_day_info(connection, day, venue_id):
    query = 'select ' + day + ' from venue_table where venue_id = ' + str(venue_id)
    data = connection.execute(query)
    return str(data) + "</br>"

if __name__ == "__main__":
    app.run(port=61004)
