from flask import request, render_template
from flask.ext.login import LoginManager, login_user, current_user, logout_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
import flask
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


@app.route('/venue_info', methods='POST')
def current_venue_info():
    return current_user.get_venue_info()


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
    query = 'select * from venue_table where email = ' + str(email)
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
    parameters = request.json
    connection = engine.connect()
    if current_user.is_authenticated():
        venue_id = current_user.venue_id
        return update_venue_by_id(connection, venue_id, parameters)
    else:
        return insert_venue(connection, parameters)

    print parameters


def insert_venue(connection, parameters):
    venue_id = randrange(0, 100000)
    query = 'insert into venue_table set'
    for key in parameters.keys():
        query += key + '=' + parameters[key] + ','
    query = query + "venue_id=" + str(venue_id)
    try:
        data = connection.execute(query)
        return data
    except Exception:
        return None


def update_venue_by_id(connection, venue_id, parameters):
    query = 'update venue_table set'
    for key in parameters.keys():
        query += key + '=' + parameters[key] + ','
    query += 'where venue_id = ' + str(venue_id)
    try:
        data = connection.execute(query)
        return data
    except Exception:
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
                return "Logged in!"
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


@app.route("/logout")
@login_required
def logout():
    if logout_user():
        return "User successfully logged out."
    else:
        return "There was an error logging out the user."


class User:

    def __init__(self, venue_info, active=True):
        if venue_info is not None:
            self.venue_name = venue_info['venue_name']
            self.address_line_1 = venue_info['address_line_1']
            self.address_line_2 = venue_info['address_line_2']
            self.city = venue_info['city']
            self.state = venue_info['state']
            self.zipcode = venue_info['zipcode']
            self.venue_phone = venue_info['venue_phone']
            self.type = venue_info['type']

            self.mon_open_hour = venue_info['mon_open_hour']
            self.mon_open_am_pm = venue_info['mon_open_am_pm']
            self.mon_close_hour = venue_info['mon_close_hour']
            self.mon_close_am_pm = venue_info['mon_close_am_pm']

            self.tues_open_hour = venue_info['tues_open_hour']
            self.tues_open_am_pm = venue_info['tues_open_am_pm']
            self.tues_close_hour = venue_info['tues_close_hour']
            self.tues_close_am_pm = venue_info['tues_close_am_pm']

            self.wed_open_hour = venue_info['wed_open_hour']
            self.wed_open_am_pm = venue_info['wed_open_am_pm']
            self.wed_close_hour = venue_info['wed_close_hour']
            self.wed_close_am_pm = venue_info['wed_close_am_pm']

            self.thurs_open_hour = venue_info['thurs_open_hour']
            self.thurs_open_am_pm = venue_info['thurs_open_am_pm']
            self.thurs_close_hour = venue_info['thurs_close_hour']
            self.thurs_close_am_pm = venue_info['thurs_close_am_pm']

            self.fri_open_hour = venue_info['fri_open_hour']
            self.fri_open_am_pm = venue_info['fri_open_am_pm']
            self.fri_close_hour = venue_info['fri_close_hour']
            self.fri_close_am_pm = venue_info['fri_close_am_pm']

            self.sat_open_hour = venue_info['sat_open_hour']
            self.sat_open_am_pm = venue_info['sat_open_am_pm']
            self.sat_close_hour = venue_info['sat_close_hour']
            self.sat_close_am_pm = venue_info['sat_close_am_pm']

            self.sun_open_hour = venue_info['sun_open_hour']
            self.sun_open_am_pm = venue_info['sun_open_am_pm']
            self.sun_close_hour = venue_info['sun_close_hour']
            self.sun_close_am_pm = venue_info['sun_close_am_pm']

            self.website = venue_info['website']
            self.yelp = venue_info['yelp']
            self.photos = venue_info['photos']
            self.other_info = venue_info['other_info']
            self.discounts = venue_info['discounts']
            self.contact = venue_info['contact']
            self.contact_phone = venue_info['contact_phone']
            self.email = venue_info['email']
            self.password = venue_info['password']
            self.venue_info = venue_info
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
        return self.venue_info

    def process_hours(self, hours):
        return hours

if __name__ == "__main__":
    app.run(port=61004)

