from flask import request, render_template
from flask.ext.login import LoginManager, login_user, current_user, logout_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
import flask
from flask import jsonify
from random import randrange

app = flask.Flask(__name__)

# Flask-login setup
SECRET_KEY = "hello? yes, this is secret key"
DEBUG = True
app.config.from_object(__name__)
login_manager = LoginManager()
login_manager.setup_app(app)

# SQLAlchemy setup
engine = create_engine('mysql://my2ooz:w3rnid@/my200z', convert_unicode=True)
db = SQLAlchemy(app)

metadata = MetaData(bind=engine)


@app.route('/main')
def main():
    return render_template("main.html")


@app.route('/login_form')
def login_form():
    return render_template("login_form.html")


@app.route('/venue_edit')
def have_code():
    return render_template("venue_edit.html")


@app.route('/venue_info', methods=['POST'])
def current_venue_info():
    return jsonify(current_user.get_venue_info())


def get_all_info(connection):
    query = 'select * from venue_table'
    data = connection.execute(query)
    return data


def get_day_info_by_venue_id(connection, day, venue_id):
    query = 'select ' + day + ' from venue_table where venue_id = ' + str(venue_id)
    try:
        data = connection.execute(query)
    except Exception:
        return None
    return data.fetchone()


def get_venue_info_by_email(connection, email):
    query = "select * from venue_table where email = '" + str(email) + "'"
    try:
        data = connection.execute(query)
    except Exception:
        return None
    return data.fetchone()


def get_venue_info_by_venue_id(connection, venue_id):
    query = 'select * from venue_table where venue_id = ' + str(venue_id)
    try:
        data = connection.execute(query)
    except Exception:
        return None
    return data.fetchone()


@app.route('/venue_update', methods=["POST"])
def update_venue():
    parameters = request.form
    connection = engine.connect()
    print parameters
    if current_user.is_authenticated():
        venue_id = current_user.venue_id
        return update_venue_by_id(connection, venue_id, parameters)
    else:
        return insert_venue(connection, parameters)


def insert_venue(connection, parameters):
    print "got this far"
    venue_id = randrange(0, 100000)
    query = 'insert into venue_table set '
    for key in parameters.keys():
        query += key + "='" + parameters[key] + "',"
    query = query + "venue_id='" + str(venue_id) + "'"
    try:
        connection.execute(query)
        return "success"
    except Exception, ex:
        print query
        print ex
        return None


def update_venue_by_id(connection, venue_id, parameters):
    query = 'update venue_table set '
    for key in parameters.keys():
        query += key + "='" + parameters[key] + "',"
    query = query[:-1] + "where venue_id='" + str(venue_id) + "'"
    try:
        connection.execute(query)
        return "success"
    except Exception, ex:
        print query
        print ex
        return None


def stringify(sql_object):
    string = str(sql_object) + "</br>"
    return string


@app.route("/login", methods=["POST"])
def login():
    if "email" in request.form and "password" in request.form:
        email = request.form["email"]
        password = request.form["password"]
        connection = engine.connect()
        venue_info = get_venue_info_by_email(connection, email)
        if venue_info is not None and venue_info['password'] == password:
            remember = request.form.get("remember", "no") == "yes"
            user = User(venue_info, active=True)
            if login_user(user, remember=remember):
                return render_template("venue_edit.html")
            else:
                return "Sorry, but we could not log you in. Please email support@my2ooz.com for help."
        else:
            return "Invalid username or password."


@login_manager.user_loader
def load_user(userid):
    connection = engine.connect()
    venue_info = get_venue_info_by_venue_id(connection, userid)
    if venue_info is None:
        return None
    else:
        return User(venue_info)


@app.route("/logout", methods=["POST"])
def logout():
    if logout_user():
        return render_template("main.html")
    else:
	print "ERROR: could not log user out!"
        return render_template("main.html")


class User:

    def __init__(self, venue_info, active=True):
        if venue_info is not None:
            self.venue_info = venue_info
            self.venue_id = venue_info['venue_id']
            self.authenticated = True
        else:
            self.authenticated = False
        self.active = active

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return self.is_authenticated

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.venue_id)

    def get_venue_info(self):
        return self.as_dict(self.venue_info)

    def process_hours(self, hours):
        return hours

    def as_dict(self, row_proxy):
       return dict(zip(row_proxy.keys(), row_proxy.values()))

if __name__ == "__main__":
    app.run(port=61004)

