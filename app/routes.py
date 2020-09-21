from app import app_obj

from flask import render_template,url_for, flash, redirect
from app.forms import RegistrationForm, LoginForm

# render_template will look for the .html files you specified
# under the templates folder. You have to name the templates folder exactly so
# flask knows where to find them

# assumes that we will be querying data from our database as dummy_data


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
    form = RegistrationForm()
    if form.validate_on_submit():       # tells us if the form is validated on submission
        flash(f"Account created for {form.username.data}!", "success") # success category is a bootstrap class to use as variable
        #flash accepts a second argument, category. So the msg above is under the success category
        # bootstrap has different alert style for successes and errors
        return redirect(url_for("home"))
    return render_template("register.html", title = "Register", form = form )

@app_obj.route('/login', methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == "password":
            flash("You have been logged in!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Please check username and password", 'danger') # bootstrap's class danger for error alert
    return render_template("login.html", title = "Login", form = form )
