from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
from datetime import datetime

class User:

    def signout(self):
        session.clear()
        return redirect('/')
    
    
    #Pass in self and a user object as parameters
    def start_session(self, user):
        
        #Removes the password from the session
        del user['password']
        
        #Flag that a user is logged in
        session['logged_in'] = True
        
        #Stores the user dictionary inside of the session
        session['user'] = user
        
        #Return the succesful status to the front end:
        #return jsonify(user), 200

        # Return user role in response
        
        return jsonify({"role": user["role"]}), 200
    
    
    #self refers to an instance of the class
    def register(self):
        print(request.form)
        
        #Creates a new user object from data collected from the html form
        user = {
            "_id": uuid.uuid4().hex,            #Generates a random unique identifier converted to a hex string
            "name": request.form.get("name"),   
            "email": request.form.get("email"), 
            "role": request.form.get("role"),
            "mobility_issue": False,
            "availability": "",   
            "password": request.form.get("password") 
        }
        
        # Encrypting the passwords so they arent stored as plaintext in the database
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        
        #Make sure email doesnt already exist inside of the database
        if db.users.find_one({ "email": user['email'] }):
            return jsonify({ "error": "Email Adress Already Registered" }), 400
        
        #This stores a new user into the users collection and returns a json response if successfull
        if db.users.insert_one(user):
            return jsonify(user), 200

        #Returns a json response indicating an error
        return jsonify({ "error": "User Registration Failed" }), 400
    
    
    def login(self):
        
        #Query database for a matching email address
        user = db.users.find_one({
            
            #Retrieves the email input from the form
            "email": request.form.get('email')
        })
        
        #If a user with that email exists a session is started
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid Login Credentials" }), 401
    
    
    def update_skills(self):
        
        #This gets us the _id of the skill we want to update
        skill_id = request.form.get('skill')
        
        
        #Get the _id of the user in session
        user_id = session.get('user').get('_id')
        
        #Go to the corresponding skill in the compsci_skills collection
        skill = db.compsci_skills.find_one({"_id": skill_id})
        if not skill:
            return jsonify({"error": "Skill not found"}), 404
        
        skill_name = skill['name']
        
        update_result = db.users.update_one(
            {"_id": user_id},
            {"$addToSet": {"skillset": skill_name}}
        )
        
        if update_result.modified_count > 0:
            
            db.compsci_skills.update_one(
                {"_id": skill_id},
                {"$addToSet": {"users": user_id}}
            )
        
            return jsonify({"success": f"Skill {skill_name} added successfully"}), 200
        else:
            return jsonify({"error": "No updates made to skills"}), 304
        
    
    def remove_skills(self):
        
        #This gets us the _id of the skill we want to remove
        skill_id = request.form.get('skill')
        
        
        #Get the _id of the user in session
        user_id = session.get('user').get('_id')
        
        #Go to the corresponding skill in the compsci_skills collection
        skill = db.compsci_skills.find_one({"_id": skill_id})
        if not skill:
            return jsonify({"error": "Skill not found"}), 404
        
        skill_name = skill['name']
        
        #Remove that skill name from the users skillset array and also remove the users _id from the users array in compsci_skills
        update_user_result = db.users.update_one(
            {"_id": user_id},
            {"$pull": {"skillset": skill_name}}  # Remove the skill name from the user's skillset
        )
        
        if update_user_result.modified_count == 0:
            return jsonify({"error": "Skill not found in user's skillset"}), 404
        
        update_skill_result = db.compsci_skills.update_one(
        {"_id": skill_id},
        {"$pull": {"users": user_id}}  # Remove the user's _id from the 'users' array in the skill document
        )
        
        if update_skill_result.modified_count == 0:
            return jsonify({"error": "User's _id not found in skill's users array"}), 404
    
        return jsonify({"success": f"Skill {skill_name} removed successfully"}), 200
        
    
    def delete_user(self):
        user = request.form.get('user_dropdown')
        print("Data from form:", user)
        
        db.users.delete_one({"name": user})
        
    
    def change_password(self):
        new_password = request.form.get("new_password")
        print("New Password:", new_password)
        print("Encryptd New Passwors", pbkdf2_sha256.encrypt(new_password))
        
        #Retrieve user _id from the session
        user_id = session.get('user').get('_id')
        
        modified = db.users.update_one(
            {"_id": user_id},
            {"$set": {"password": pbkdf2_sha256.encrypt(new_password)}}
        )
        
        if modified.modified_count == 1:
            return jsonify({"success": "Password updated successfully"}), 200
        else:
            return jsonify({"error": "No changes made to the password"}), 400
        
        
    def toggle_mobile(self):
        form_data = request.form.get("toggle")
        print("Form Data:", form_data)

        #Retrieve user _id from the session
        user_id = session.get('user').get('_id')
        
        if form_data == "yes":
            result = db.users.update_one(
            {"_id": user_id},  # Ensure user_id is correctly formatted as ObjectId
            {"$set": {"mobility_issue": True}}
        )
            
        else:
            result = db.users.update_one(
            {"_id": user_id},  # Ensure user_id is correctly formatted as ObjectId
            {"$set": {"mobility_issue": False}}
        )
            
        
        return jsonify({"success": "this worked"}), 200
    
    
    def set_availability(self):
        
        availability_date = request.form.get('availability_date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        
        start_datetime_str = f"{availability_date} {start_time}"
        end_datetime_str = f"{availability_date} {end_time}"
        
        start_date = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
        end_date = datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M")

        
        #Retrieve user _id from the session
        user_id = session.get('user').get('_id')
        
        
        #Availability document
        availability = {
            "_id": uuid.uuid4().hex,
            "user_id" : user_id,
            "start_time": start_date,
            "end_time": end_date
        }
        
        db.availability.insert_one(availability)
        
        
        return jsonify(success=True, message="Avaiability Updated")
    
    
    def add_new_skill(self):
        new_skill = request.form.get('new_skill')
    
        
        existing_skill = db.compsci_skills.find_one({"name": new_skill})
        
        if existing_skill:
            return jsonify(success=False, message="Skill already exists in collection"), 409
        
        new_skill_doc = {
            "_id": uuid.uuid4().hex,
            "name": new_skill,
            "users": []
        }
        
        db.compsci_skills.insert_one(new_skill_doc)
    
        return jsonify(success=True, message="Skill added successfully!")
        
    def admin_remove_skill(self):
        
        #Gets the _id of the skill we want to remove
        skill_id = request.form.get('skill')
        

        skill = db.compsci_skills.find_one({"_id": skill_id})
        

        # Remove skill from compsci_skills collection
        db.compsci_skills.delete_one({"_id": skill_id})
        
        #Remove the skill from all users' skillset
        db.users.update_many(
            {},  # This means all users
            {"$pull": {"skillset": skill['name']}}  # Remove skill by name
        )
        
        return jsonify({"success": f"Skill '{skill}' removed successfully"}), 200
        
    
    
    #This is now working for dropping the availability, still need to make adjustments to the front end...
    #so that when when the availability is dropped you dont need to refresh the page to see the changes
    #Another option is to take away the code stopping the page from refreshing, need to look into what the better option is
    def drop_availability(self):
        
        availability_id = request.form.get('_id')
        
        db.availability.delete_one({"_id": availability_id})
        
        return jsonify(availability_id, "dropped")
        
        
    def add_building(self):
        
        new_building = request.form.get("new_building")
        floors = int(request.form.get("floors"))
        
        new_building_doc = {
            "_id": uuid.uuid4().hex,
            "name": new_building,
            "floors": floors,
            "travel_times": {}
        }
        
        db.buildings.insert_one(new_building_doc)
        
        
        return jsonify({"success": True, "message": "New Building Stored Successfully", "new_building": new_building_doc})
    
    def remove_building(self):
        
        building_id = request.form.get("building")
        print("Building _id:", building_id)
        
        db.buildings.delete_one({"_id": building_id})
        
        #Remove all travel times involving the building thats getting removed
        db.travel_times.delete_many({"$or": [{"building_a": building_id}, {"building_b": building_id}]})

        
        return jsonify(success=True, message="Building Removed from Database Successfully")
    
    
    def set_travel_time(self):
        
        travel_times = {}
        
        for key, value in request.form.items():
            if key.startswith('travel_time'):
                # Example key format: travel_time[new_building_name][other_building_id]
                parts = key.split('][')
                new_building_id = str(parts[0].split('[')[1])  # Extract new building _id
                other_building_id = str(parts[1][:-1])  # Extract other building id (remove the last ']')
                
                # Store the travel time in the dictionary
                if new_building_id not in travel_times:
                    travel_times[new_building_id] = {}
                    
                travel_times[new_building_id][other_building_id] = int(value)
        
        
                    
        form_data = request.form
        print("Form Data:", form_data)
        print("Travel Times:", travel_times)
        print("new_building_id:", new_building_id)
        
        travel_times_to_insert = []
        for new_building_id, times in travel_times.items():
            for other_building_id, travel_time in times.items():
                travel_times_to_insert.append({
                    "_id": uuid.uuid4().hex, 
                    "building_a": new_building_id,
                    "building_b": other_building_id,
                    "travel_time": travel_time
                })
                travel_times_to_insert.append({
                    "_id": uuid.uuid4().hex, 
                    "building_a": other_building_id,
                    "building_b": new_building_id,
                    "travel_time": travel_time
                })  # Store bidirectional travel times

        if travel_times_to_insert:
            db.travel_times.insert_many(travel_times_to_insert)
        
        
        return jsonify(success=True, message="Times Updated Successfully")
        
            
    def request_support(self):
            
        date = request.form.get("availability_date")
        skills = request.form.getlist("skills[]")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        building_id = request.form.get("building")
        floor = request.form.get("floor")
        room = request.form.get("room")
        
        
        
        print("Data from form:", date, skills, start_time, end_time, building_id, floor, room)
        
        return jsonify(success=True, message="Form Data sent successfully")
        
        
        
    
   
        
        
        
        
        
        
        
        
    



        
    
    
 
        
        
        