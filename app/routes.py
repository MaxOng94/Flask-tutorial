from app import app_obj
from flask import render_template
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
