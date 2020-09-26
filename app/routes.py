from app import app_obj, db, bcrypt, mail
from flask import render_template,url_for, flash, redirect , request, abort
from forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                    PostForm, RequestResetForm, PasswordResetForm)
from PIL import Image
# render_template will look for the .html files you specified
# under the templates folder. You have to name the templates folder exactly so
# flask knows where to find them

from flask_login import login_user,current_user, logout_user, login_required
# assumes that we will be querying data from our database as dummy_data
from datetime import datetime
import secrets
import os
from models import User, Post

from flask_mail import Message
# =====================
# route for HOME PAGE
"""
1) HOME()
2) ABOUT()
3) REGISTER()
"""
@app_obj.route('/')
@app_obj.route('/home', methods = ["GET","POST"])
def home():
    page = request.args.get('page', 1, type = int)          #  1 : the default page number, and type = int --> will throw in error if someone else throws in non-int for page number
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 4)  # basically limiting 4 posts per page
    return render_template('home.html', posts = posts)

@app_obj.route('/about')
def about():
    return render_template('about.html', title = "About")

@app_obj.route('/register', methods = ["GET","POST"])
def register():
    if current_user.is_authenticated: #current_user is from login_manager, it remembers if we are current_user (already logged in)
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
# ==========================


# =====================
# route for lOGIN PAGE
"""
1) LOGIN()
2) LOGOUT()
"""

@app_obj.route('/login', methods = ["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))    #if already logged in, everytime they want to log in, we return them to home page
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

#===================================


# =====================
# route for ACCOUNT PAGE

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
    image_file = url_for('static', filename = "profile_pics/" + current_user.image_file) # image file in the models module under User class. It is in the database
    return render_template("account.html", title = "Account", image_file = image_file, form = form)

# ================================



# ===================================
# route for POST PAGE

"""
1) NEW_POST()
2) POST()
3) UPDATE() --> to update the post title and content
    - added condition that ONLY author can update their own post
4) DELETE_POST()
    - added condition that ONLY author can update their own post
    - a modal will pop up when authors want to delete their own posts
5) USER_POSTS()
    - to return only all the posts written by user
"""
@app_obj.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title =form.title.data, content =form.content.data, author = current_user)
        db.session.add(new_post)
        db.session.commit()
        flash(f"New post '{form.title.data}' created!", "success") # success category is a bootstrap class to use as variable
        return redirect(url_for('home'))
    return render_template("create_post.html", title = "New Post", form = form,
                            legend = 'New Post')

@app_obj.route('/post/<int:post_id>', methods = ['GET','POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post = post)

@app_obj.route('/post/<int:post_id>/update', methods = ['GET','POST'])
@login_required
def update(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f"Your post '{form.title.data}' has been updated!", "success") # success category is a bootstrap class to use as variable
        return redirect(url_for('post', post_id = post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', form = form, post = post,
                            legend = 'Update Post')


@app_obj.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash(f"Your post '{form.title.data}' has been deleted!", "success") # success category is a bootstrap class to use as variable
        return redirect(url_for('home'))
    return render_template('create_post.html', form = form, post = post,
                            legend = 'Update Post')


@app_obj.route('/user/<string:username>', methods = ["GET","POST"])
def user_posts(username):
    page = request.args.get('page', 1, type = int)          #  1 : the default page number, and type = int --> will throw in error if someone else throws in non-int for page number
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author = user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page = page, per_page = 4)  # basically limiting 4 posts per page
    return render_template('user_posts.html', posts = posts, user = user)

#==============================================
# reset request

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app_obj.route('/reset_password', methods = ["GET","POST"])
def reset_request():
    if current_user.is_authenticated: #current_user is from login_manager, it remembers if we are current_user (already logged in)
        return redirect(url_for("home"))  # so if we try to click register as a current user, we re-direct them back to home page
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title = 'Reset Password',form = form)


@app_obj.route('/reset_password/<token>', methods = ["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated: #current_user is from login_manager, it remembers if we are current_user (already logged in)
        return redirect(url_for("home"))  # so if we try to click register as a current user, we re-direct them back to home page
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():       # tells us if the form is validated on submission
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title = 'Reset Password', form = form)
