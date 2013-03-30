from flask import request, render_template
from flask.ext.login import LoginManager, login_user, current_user, logout_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
import flask

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


@app.route("/main")
def main():
    return render_template("main.html")


@app.route('/login_form')
def login_form():
    return render_template("login_form.html")


@app.route("/passcode_check")
def passcode_check():
    return render_template("passcode_check.html")


@app.route("/have_code")
def have_code():
    return render_template("have_code.html")


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
    print final_string
    print "current user: " + str(current_user)
    # END TESTS


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


def get_venue_info_by_login(connection, login):
    query = 'select * from venue_table where login = ' + str(login)
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


@app.route('/update_venue', methods='POST')
def update_venue(connection, venue_id, parameters):
    connection = engine.connect()
    venue_id = current_user.venue_id
    parameters = request.json
    print parameters
    return update_venue_by_id(connection, venue_id, parameters)


def update_venue_by_id(connection, venue_id, parameters):
    query = 'update venue_table set'
    for key in parameters.keys():
        query += key + '=' + parameters[key] + ','
    query += 'where venue_id = ' + str(venue_id)


def stringify(sql_object):
    string = str(sql_object) + "</br>"
    return string


@app.route("/login", methods=["GET", "POST"])
def login():
    if "login" in request.form and "password" in request.form:
        login = request.form["login"]
        password = request.form["password"]
        connection = engine.connect()
        venue_info = get_venue_info_by_login(connection, login)
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

if __name__ == "__main__":
    app.run(port=61004)
