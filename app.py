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
            #Check if user is logged in, if not logged in redirect to login page
            if not session.get('logged_in') or 'user' not in session:
                return redirect('/')  # Redirect to login page

            #Check if user has the required role
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
    
    #find the _id and name of each skill inside the collection
    compsci_skill_cursor =  db.compsci_skills.find({}, {"_id": 1, "name": 1})
    
    #Store results in a dictionary
    compsci_skills = [{"_id": skill["_id"], "name": skill["name"]} for skill in compsci_skill_cursor]
    
    print(compsci_skills)
    
    

    #Get the _id of the user in session
    user_id = session.get('user').get('_id')
    role = session.get('user').get('role')
    
    
    #Query the skillset of appropriate _id from collection users
    user = db.users.find_one({"_id": user_id})
    skills = user.get('skillset', [])
    
    availability = list(db.availability.find({"user_id": user_id}))
    
    
    availability_data = []

    for slot in availability:
        # Extract date as YYYY-MM-DD from 'date' or 'start_time'
        date_str = slot.get('date') or slot.get('start_time')  # Use 'start_time' if 'date' is missing
        date_str = date_str.strftime('%Y-%m-%d')  # Convert datetime to string

        availability_data.append({
            "_id": slot['_id'],
            "date": date_str,
            "start_time": slot['start_time'].strftime('%H:%M'),  # Convert time to HH:MM
            "end_time": slot['end_time'].strftime('%H:%M')       # Convert time to HH:MM
        })
    
    
    return render_template('ta.html', skills=skills, availability=availability, availability_data=availability_data, compsci_skills=compsci_skills, role=role)

@app.route('/ml/')
@login_required(role="Module Leader")
def ml():
    
    user_id = session.get('user').get('_id')
    role = session.get('user').get('role')
    
    
    return render_template('ml.html', role=role, user_id=user_id)

@app.route('/admin/')
@login_required(role="Admin")
def admin():
    
    all_users = db.users.find({}, {"_id": 1, "name": 1})
    user_names = [user['name'] for user in all_users]
    
    

    return render_template('admin.html', user_names = user_names)

@app.route('/unauthorized/')
def unauthorized():
    return render_template('unauthorized.html')











