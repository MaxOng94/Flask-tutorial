from app import app_obj, db, bcrypt
from flask import render_template,url_for, flash, redirect , request
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from models import User
from PIL import Image
# render_template will look for the .html files you specified
# under the templates folder. You have to name the templates folder exactly so
# flask knows where to find them

from flask_login import login_user,current_user, logout_user, login_required
# assumes that we will be querying data from our database as dummy_data

import secrets
import os
dummy_data = [
    {
        'author': 'Max ong',
        'title' : 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'April 20 2020'
    },
    {
        'author': 'Max ong',
        'title' : 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'April 20 2020'
    }
]




@app_obj.route('/')
@app_obj.route('/home')
def home():
    return render_template('home.html', posts = dummy_data)

@app_obj.route('/about')
def about():
    return render_template('about.html', title = "About")

@app_obj.route('/register', methods = ["GET","POST"])
def register():
    if current_user.is_authenticated: #from login_manager, it remembers if we are current_user (already logged in)
        return redirect(url_for("home"))  # so if we try to click register as a current user, we re-direct them back to home page

    form = RegistrationForm()

    if form.validate_on_submit():       # tells us if the form is validated on submission
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash(f"Account created for {form.username.data}! You can now log in.", "success") # success category is a bootstrap class to use as variable
        #flash accepts a second argument, category. So the msg above is under the success category
        # bootstrap has different alert style for successes and errors
        return redirect(url_for("login"))
    return render_template("register.html", title = "Register", form = form )

@app_obj.route('/login', methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # just checking from User class if
                                                                    #the email user logged in with already exist in db
        if user and bcrypt.check_password_hash(user.password, form.password.data):  #user.password checks the db if the hashed password
                                                                                    #is the same as the password user inputs in login password field
            login_user(user,remember = form.remember.data)
            next_page = request.args.get("next")  # gets the next paramter from the login next_page
                                                    # get method retreives from the args dictionary
            return redirect(url_for('home')) if next_page else redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Please check email and password", 'danger') # bootstrap's class danger for error alert
    return render_template("login.html", title = "Login", form = form )


@app_obj.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)        # randomize the image name of the picture so not to collide with existing pictures in our db
    _, f_ext = os.path.splitext(form_picture.filename)   # use secrets module to generate random hex for the file name of pictures
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app_obj.root_path, 'static/profile_pics',picture_fn)

    # image resizing
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app_obj.route('/account', methods = ["GET","POST"])
@login_required         # with this decorator, this means to access this view, users has to be logged in already
def account():
    image_file = url_for('static', filename = "profile_pics/" + current_user.image_file) # image file in the models module under User class. It is in the database
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data  # updating the information in the database, it is just changing the variables
        current_user.email = form.email.data
        db.session.commit()
        flash("your account has been updated!", "success")
        return redirect (url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title = "Account", image_file = image_file, form = form)
