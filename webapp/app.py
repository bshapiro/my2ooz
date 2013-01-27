#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

engine = create_engine('mysql://@/test', convert_unicode=True)

app = flask.Flask(__name__)
app.debug = True
db = SQLAlchemy(app)

@app.route("/")
def hello():
    connection = engine.connect()
    data = connection.execute('select * from SITES')
    connection.close()
    string = ""
    for row in data:
        string += str(row) + "</br>"
    return string

if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
