from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app_obj = Flask(__name__)
from app import routes

# secret key to protect against modifying cookies and cross site forgery attacks
app_obj.config["SECRET_KEY"] = 'baf2822cca9a24b261cd4d04c2976373'
app_obj.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
# relative path from the current file.
# this means that we need to have a site.db file alongside this init file we are in

db = SQLAlchemy(app_obj)
