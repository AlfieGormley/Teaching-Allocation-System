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


def login_required(role=None):
    
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            #Check if user is logged in
            if not session.get('logged_in') or 'user' not in session:
                return redirect('/')  # Redirect to login page

            #Check if user has the required role (if applicable)
            if role and session['user'].get('role') != role:
                return redirect('/unauthorized/')  # Redirect to unauthorized page


            return f(*args, **kwargs)
        return wrap
    return decorator


            
#Routes
from user import routes

#Route to home
@app.route('/')
def home():
    return render_template('login.html')

#Route to the dashboard, having the second / means theres only one route users can access
@app.route('/ta/')
@login_required(role="Teaching Associate")
def ta():
    return render_template('ta.html')

@app.route('/ml/')
@login_required(role="Module Leader")
def ml():
    return render_template('ml.html')

@app.route('/admin/')
@login_required(role="Admin")
def admin():
    return render_template('admin.html')

@app.route('/unauthorized/')
def unauthorized():
    return render_template('unauthorized.html')







