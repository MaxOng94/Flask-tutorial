from flask import Flask
app_obj = Flask(__name__)
from app import routes

# secret key to protect against modifying cookies and cross site forgery attacks
app_obj.config["SECRET_KEY"] = 'baf2822cca9a24b261cd4d04c2976373'


# added Regristration and login form for our site
# added secret key from app config
