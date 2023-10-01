from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS with credentials support

SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://{username}:{password}@{hostname}/{databasename}".format(
    username="Timi1234",
    password="",
    hostname="Timi1234.mysql.pythonanywhere-services.com",
    databasename="Timi1234$database_name"
)
app.config['DEBUG'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SECRET_KEY'] = '02ff7dc692594b26fedb715e'

db = SQLAlchemy(app)

from package import routes
