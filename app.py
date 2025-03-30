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
    
    #Collect User ID from session
    user_id = session.get('user').get('_id')
    
    #Collect Role from session
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
    
    #Collects all shift data for the user_id?
    shift_docs = list(db.shifts.find({"ta_id": user_id}))
        
    #Format Shift data to send to front end
    formatted_shifts = []
    for shift in shift_docs:
        formatted_shifts.append({
            "shift_id": shift["_id"],
            "ta_id": shift["ta_id"],
            "ml_id": shift["ml_id"],
            "date": shift["date"],
            "start_time": shift["start_time"].strftime("%H:%M"),
            "end_time": shift["end_time"].strftime("%H:%M"),
            "room": shift["room"],
            "building": shift["building"],
            "floor": shift["floor"],
            "description": shift["description"],
            "status": shift["status"]
            })
    
    
    return render_template('ta.html', skills=skills, availability=availability, availability_data=availability_data, compsci_skills=compsci_skills, role=role, formatted_shifts=formatted_shifts)

@app.route('/ml/')
@login_required(role="Module Leader")
def ml():
    
    #find the _id and name of each skill inside the collection
    compsci_skill_cursor =  db.compsci_skills.find({}, {"_id": 1, "name": 1})
    
    #Store results in a dictionary
    compsci_skills = [{"_id": skill["_id"], "name": skill["name"]} for skill in compsci_skill_cursor]
    
    buildings_cursor = db.buildings.find({}, {"_id": 1, "name": 1, "floors": 1})
    
    buildings = [{"_id": building["_id"], "name": building["name"], "floors": building["floors"]} for building in buildings_cursor]
    
    #Collect User ID from session
    user_id = session.get('user').get('_id')
    
    #Collect Role from session
    role = session.get('user').get('role')
    
    #Collects all shift data for the user_id?
    shift_docs = list(db.shifts.find({"ml_id": user_id}))
        
    #Format Shift data to send to front end
    formatted_shifts = []
    for shift in shift_docs:
        formatted_shifts.append({
            "shift_id": shift["_id"],
            "ta_id": shift["ta_id"],
            "ml_id": shift["ml_id"],
            "date": shift["date"],
            "start_time": shift["start_time"].strftime("%H:%M"),
            "end_time": shift["end_time"].strftime("%H:%M"),
            "room": shift["room"],
            "building": shift["building"],
            "floor": shift["floor"],
            "description": shift["description"],
            "status": shift["status"]
            })
    
    print(formatted_shifts)
    
    
    
    
    #Send approved shifts with ml_id = user_id
    
    
    
    return render_template('ml.html', role=role, user_id=user_id, compsci_skills=compsci_skills, buildings=buildings, formatted_shifts=formatted_shifts)

@app.route('/admin/')
@login_required(role="Admin")
def admin():
    
    #Query shifts collection for pending shifts
    pending_shift_docs = db.shifts.find({"status": "pending"})
    
    pending_shifts = []
    
    for shift in pending_shift_docs:
        
        #Look up the module leader
        ml_data = db.users.find_one({"_id": shift["ml_id"]})
        
        #Extract ML name
        ml_name = ml_data["name"]
        
        ta_id = shift["ta_id"]
        
        #If TA has been asigned
        if ta_id != "Not Yet Assigned":
            
            #Look up the TA
            ta_data = db.users.find_one({"_id": shift["ta_id"]})
            
            #Extract TA name
            ta_name = ta_data["name"]
        
        else: 
            ta_name = "Not Yet Assigned"
            
        #Look up the building
        building_data = db.buildings.find_one({"_id": shift["building"]})
        
        #Look up Building name
        building_name = building_data["name"]
        
        shift_data = {
            "shift_id": shift["_id"],
            "ml_name": ml_name,
            "ta_name": ta_name,
            "date": shift["date"],
            "start_time": shift["start_time"],
            "end_time": shift["end_time"],
            "building_name": building_name,
            "room_name": shift["room"],
            
        }
        
        pending_shifts.append(shift_data)
        
    
    #find the _id and name of each skill inside the collection
    compsci_skill_cursor =  db.compsci_skills.find({}, {"_id": 1, "name": 1})
    
    #Store results in a dictionary
    compsci_skills = [{"_id": skill["_id"], "name": skill["name"]} for skill in compsci_skill_cursor]
    
    buildings_cursor = db.buildings.find({}, {"_id": 1, "name": 1})
    
    buildings = [{"_id": building["_id"], "name": building["name"]} for building in buildings_cursor]
    
    all_users = db.users.find({}, {"_id": 1, "name": 1})
    
    user_names = [user['name'] for user in all_users]
    
    

    return render_template('admin.html', user_names = user_names, compsci_skills=compsci_skills, buildings=buildings, pending_shifts=pending_shifts)

@app.route('/unauthorized/')
def unauthorized():
    return render_template('unauthorized.html')











