from app import db, login_manager, app_obj
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # makes sure the user_id is an int


class User(db.Model, UserMixin): # what is db.Model?
    id = db.Column(db.Integer, primary_key = True)

    username = db.Column(db.String(20), unique = True, nullable =False)
    # db.string(20)--> data type is string and needs to be 20 chars long
    # unique = True --> must be unique, nullable = False --> cannot be null

    email = db.Column(db.String(120), unique = True, nullable =False)

    image_file = db.Column(db.String(20), nullable=False, default ='default(1).jpg')

    password = db.Column(db.String(60), nullable=False)
    # hashing algorithm will hash the password into 60 chars, does not mean we want password to be 60 chars

    posts = db.relationship("Post", backref ='author', lazy =True)
    # post attribute has a relationship to the Post model
    # backref --> similar to adding a column to Post model. So when we have a post, we can use the author
    # attribute to get user who created the post
    # lazy justifies when sqlalchemy load data from db, and sqlalchemy will load the data at one go.

    def get_reset_token(self, expires_sec= 1800):
        s = Serializer(app_obj.config['SECRET_KEY'], expires_sec)
        return s.dumps({"user_id": self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app_obj.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):     # similar to __str__, how the obj is printed when we print the obj out
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(100), nullable =False)

    date_posted = db.Column(db.DateTime, nullable = False, default= datetime.today)

    content = db.Column(db.Text, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    # get the user id from User model
    # foreign key is referencing the table and column name from User, which will automatically set the id from User model to lower case.

    def __repr__(self):     # similar to __str__, how the obj is printed when we print the obj out
        return f"User('{self.title}','{self.date_posted}')"
