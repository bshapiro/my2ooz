from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
from sqlalchemy import create_engine
engine = create_engine('mysql://allie:967enm/allie', convert_unicode=True)

db = SQLAlchemy(app)


@app.route("/")
def hello():
    connection = engine.connect()
    data = connection.execute('select * from sites')
    connection.close()
    string = ""
    for row in data:
        string += row + "</br>"
    return string

if __name__ == "__main__":
    app.run()