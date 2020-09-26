from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app_obj = Flask(__name__)

# secret key to protect against modifying cookies and cross site forgery attacks
app_obj.config["SECRET_KEY"] = 'baf2822cca9a24b261cd4d04c2976373'
app_obj.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
# relative path from the current file.
# this means that we need to have a site.db file alongside this init file we are in

db = SQLAlchemy(app_obj)
bcrypt = Bcrypt(app_obj)
login_manager = LoginManager(app_obj)
login_manager.login_view = "login" # function name for our login route, same as url_for()
login_manager.login_message_category = "info"
app_obj.config['MAIL_PORT'] = 587
app_obj.config['MAIL_SERVER'] = 'smtp.gmail.com'
app_obj.config['MAIL_USE_TLS'] = True
app_obj.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app_obj.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
mail = Mail(app_obj)




from app import routes
