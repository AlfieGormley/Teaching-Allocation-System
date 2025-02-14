from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo

#Create an instance of the app
app = Flask(__name__)

#Secret key needed for sessions
app.secret_key = b"\x1a\xe2\xf9\x01K8'\xa7\x8c\x12\xddS\x88\x80R\xe1"

#Database
client = pymongo.MongoClient("localhost", 27017)
db = client.TAS

#It must not be entering the first if statement if we are being redirected to the home page every time.
#Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
        
    return wrap
            


#Routes
from user import routes

#Route to home
@app.route('/')
def home():
    return render_template('login.html')

#Route to the dashboard, having the second / means theres only one route users can access
@app.route('/ta/')
@login_required
def ta():
    return render_template('ta.html')

@app.route('/ml/')
@login_required
def ml():
    return render_template('ml.html')

@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')





