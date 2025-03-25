from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
from datetime import datetime
import pytz
from collections import defaultdict
import random

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
        
    #Get TAs who have the desired skill set
    def get_ta_candiates(self, skills):
        
        #Collect the appropriate skill documents
            skill_docs = list(db.compsci_skills.find({"_id": {"$in": skills}}))
            
            #Extract the user list for each skill
            user_sets = [set(skill["users"]) for skill in skill_docs]
            
            #Collect users who appear in all lists.
            return set.intersection(*user_sets) if user_sets else set()
    
    #Gets TAs with mobility issues matching the desired skill set
    def get_disabled_ta_candidates(self, skills):
        
        #Collect the appropriate skill documents
            skill_docs = list(db.compsci_skills.find({"_id": {"$in": skills}}))
            
            #Extract the user list for each skill
            user_sets = [set(skill["users"]) for skill in skill_docs]
            
            #Collect users who appear in all lists.
            ta_candidates = set.intersection(*user_sets) if user_sets else set()
            
            #Filter for TAs who have mobility issues
            disabled_candidates = {
                ta for ta in ta_candidates 
                if db.users.find_one({"_id": ta, "mobility_issue": True})
            }
            
            return disabled_candidates
            
    #Convert date to ISODate Format and Localise with the timezone
    def convert_to_iso(self, requested_date, start_time, end_time):
        
        #Set timezone
        timezone = pytz.timezone("UTC")
        
        #Convert to ISODate Format
        start_time_iso = datetime.strptime(f"{requested_date} {start_time}", "%Y-%m-%d %H:%M")
        end_time_iso = datetime.strptime(f"{requested_date} {end_time}", "%Y-%m-%d %H:%M")
        
        #Localise with the time zone
        start_time_iso = timezone.localize(start_time_iso)
        end_time_iso = timezone.localize(end_time_iso)
        
        return start_time_iso, end_time_iso
    
    #Collect available TAs from a set of candidates
    def get_available_tas(self, ta_candidates, start_time_iso, end_time_iso):
        
        #Set to store TAs with matching availability
        available_tas = set()
        
        #Collect the relevent availability docs
        ta_availability_docs = list(db.availability.find({
                "user_id": {"$in": list(ta_candidates)},
                "start_time": {"$lte": start_time_iso},
                "end_time": {"$gte": end_time_iso}
            }))
        
        #Extract the user_id from the availability docs and add to available_tas
        for doc in ta_availability_docs:
            available_tas.add(doc["user_id"])
        
        return available_tas
    
    #Returns the rarity of each skill in a ranking system
    def skill_rankings(self):
        
        #Collects all skill documents
        all_skill_docs = list(db.compsci_skills.find({}))
        
        #Count the number of users for each skill
        skill_counts = {skill["_id"]: len(skill["users"]) for skill in all_skill_docs}
            
        #Calculate the rarity of each skill (Higher rarity = more unique skill)
        skill_rarity = {skill_id: 1 / count if count > 0 else 1 for skill_id, count in skill_counts.items()}
        
        return skill_rarity, all_skill_docs
    
    #Will rank and sort TAs according to skill_rarity
    def ta_scores(self, available_tas, all_skill_docs, skill_rarity):
        
        #Default Dictonary for storing TAs uniquness score
        ta_scores = defaultdict(float)
            
        #Iterate over each ta who is available and has the matching skill set
        for user_id in available_tas:
            #Loops through all skills stored in compsci_skills
            for skill in all_skill_docs:
                #If the current TA appears in the user list for that skill
                if user_id in skill["users"]:
                    #Add the rarity score for this skill to the TAs uniqueness score
                    ta_scores[user_id] += skill_rarity[skill["_id"]]
        
        return sorted(ta_scores.items(), key=lambda x: x[1])
    
    
    
    #Removes available TAs whose schedule doesnt allow time to commute
        #THOUGHTS NEED TO CHECK IF IN SAME BUILDING, need to know the structure of the shifts collection
        #Consider for diabled TAs if they do need to commute we need to adjust their commute times
    def filter_available_tas(self, floor, start_time, available_tas):
        
        #This variable needs to be thought about slightly more:
        #floor_travel_time = 20 seconds
        
        #Iterate through available_tas "user_id"
            #Collect shift_records on the same date
                #if len(shift_records) == 0:

                    #return ("No TAs Removed")
                
                #commute = (sheduled_floor + floor) * floor_travel_time
                
                #Assess each shift record to esnure it doesnt prevent the tas availability
                    #Result = (scheduled_end_time + commute) < start_time
                        
                    
        
        
        return
    
    def exctract_request_form(self):
        
        #Need to send this data to admin.html along with the most suitable TA
        requested_date = request.form.get("availability_date") 
        skills = request.form.getlist("skills[]")
        start_time = request.form.get("start_time") 
        end_time = request.form.get("end_time")
        building_id = request.form.get("building") 
        floor = request.form.get("floor")
        room = request.form.get("room")
        description = request.form.get("description")
        
        return requested_date, skills, start_time, end_time, building_id, floor, room, description
    
    def set_operation_mode():
        
        operation_mode = request.form.get("operation_mode")
        print("Operation Mode:", operation_mode)
        
        #(0) If collection is empty/doesnt exists
        if db.operation_mode.count_documents({}) == 0:
            
            #Create mode directly
            db.operation_mode.insert_one({
                "_id": uuid.uuid4().hex,
                "operation_mode": operation_mode,
                "active": True
            })
            return jsonify(success=True, message=f"Operation mode {operation_mode} is now active")

        
        #(1): Set currently active operation mode to False
        db.operation_mode.update_one(
            {"active": True},  # Find the currently active mode
            {"$set": {"active": False}}  # Set it to inactive
        )
        
        #(2) Check if operation_mode exists in the collection
        existing_mode = db.operation_mode.find_one({"operation_mode": operation_mode})
        
        #If operation_mode exists
        if existing_mode:
            #Update to mode active
            db.operation_mode.update_one(
                {"operation_mode": operation_mode},
                {"$set": {"active": True}}
            )
            
        #If it doesn’t exist
        else: 
            #Create mode document
            db.operation_mode.insert_one({
                "_id": uuid.uuid4().hex,
                "operation_mode": operation_mode,
                "active": True
            })
        

        return jsonify(success=True, message=f"Operation mode {operation_mode} is now active")
    
    
    #NOTES ON THE ALGORITHM:
    
    #(1) - After Admin approval variable changes effect pending requests results
    
    #(2) - Consider Maxmium/Minumum Work Quotas
    
    #(3) - Consider no TA's matching requirements
    
    #(4) - If no TAs available: 
    #           Store list of close candidates who could be considered if the quota isnt matched
    
    #(5) - Maybe on ML form, if no available_tas, what degree of lateness would be acceptable?
    
    def request_support(self):
        
        #Collect Module Leader _id from the sessio
        ml_id = session.get('user').get('_id')
        
        #Collect the currently active operation mode document
        active_mode_doc = db.operation_mode.find_one({"active": True})
        
        #Assign operation mode
        operation_mode = int(active_mode_doc["operation_mode"])
        
        #Extract data from the request form
        requested_date, skills, start_time, end_time, building_id, floor, room, description = User.exctract_request_form(self)
        
        start_time_iso , end_time_iso = User.convert_to_iso(self, requested_date, start_time, end_time)
        
        
        #If room is on the ground floor:
        if floor == "G":
            print("Searching for Disbaled TAs With Suitable Availability")
            
            #Collect TAs with mobility issues matching the desired skill set
            ta_candidates = User.get_disabled_ta_candidates(self, skills)
            
            #Convert start and end time to ISODate format and localise with timezone
            start_time_iso , end_time_iso = User.convert_to_iso(self, requested_date, start_time, end_time)
            
            #Collect the ta_candidates with matching availablility
            available_tas = User.get_available_tas(self, ta_candidates, start_time_iso, end_time_iso)
            
            #Remove TAS who CAN'T from available_tas
            #Remove TAS who CAN'T from available_tas
            #Remove TAS who CAN'T from available_tas
                
            #Collect all the skill documents and calculate their rarity
            skill_rarity, all_skill_docs = User.skill_rankings(self)
            
            #Sorts the available TAs according to skill_rarity, first in list = lowest uniquness
            sorted_tas = User.ta_scores(self, available_tas, all_skill_docs, skill_rarity)
            
            #Select the TA with the lowest uniqueness score
            best_ta = sorted_tas[0][0] if sorted_tas else None
            
            

            
            #Get TAs who have the desired skill set with mobility issues
            return print("Disabled Candidates:", ta_candidates)
            
        #Mode to randomise TA selection out of the available TAs matching the skill set 
        elif operation_mode == 1:
            print("Running Operation Mode 1")
            
            #Get TAs who have the desired skill set
            ta_candidates = User().get_ta_candiates(skills)
            
            #Convert start and end time to ISODate format and localise with timezone
            #start_time_iso , end_time_iso = User.convert_to_iso(self, requested_date, start_time, end_time)
            
            #Collect ta_candidates with matching availablility
            available_tas = list(User.get_available_tas(self, ta_candidates, start_time_iso, end_time_iso))
            
            #Remove TAS who CAN'T from available_tas
            #Remove TAS who CAN'T from available_tas
            #Remove TAS who CAN'T from available_tas
            
            #Randomly select a candidate
            best_ta = random.choice(list(available_tas))
            
            print("Randomly selected TA candidate:", best_ta)
            
            
            
        #Mode in which admin grants approval pre TA allocation
        elif operation_mode == 2:

            print("Running Operation Mode 2")
            
            #Create shift document for admin approval
            shift_doc = {
                "_id": uuid.uuid4().hex,
                "ta_id": "Not Yet Assigned",
                "ml_id": ml_id,
                "date": requested_date,
                "start_time": start_time_iso,
                "end_time": end_time_iso,
                "room": room,
                "building": building_id,
                "floor": floor,
                "description": description,
                "skills": skills,
                "operation_mode": operation_mode,
                "time_stamp": datetime.now(),
                "status": "pending"  #Could be: "pending", "approved", "rejected", "completed"
            }
            
            #Store the document in the shifts collection
            db.shifts.insert_one(shift_doc)
            
            
            
            
            
            
        #Mode in which admin can select candidate based on a specific quota (TA information will have to be displayed)
        elif operation_mode == 3:
            
            print("Running Operation Mode 3") 
        
        
        #Mode in which admin grants approval post TA allocation (Much slower, queue needed must be done one at a time)
        elif operation_mode == 4:
            print("Running Operation Mode 4")
            print("Searching for TAs With Suitable Availability and skill set")
            
            #Get TAs who have the desired skill set
            ta_candidates = User().get_ta_candiates(skills)
            
            #Convert start and end time to ISODate format and localise with timezone
            #start_time_iso , end_time_iso = User.convert_to_iso(self, requested_date, start_time, end_time)
            
            #Collect ta_candidates with matching availablility
            available_tas = User.get_available_tas(self, ta_candidates, start_time_iso, end_time_iso)
            
            
            #Out of available_tas who can make it factoring commute time
            #(We essentially need to check if the end-time of their last shift + commute time <= start_time of this shift)
            #For every user_id in available_tas
                #Search Shifts where 
                    #date = requested_date
                    #pending = FALSE
                    
                    
            #Remove TAS who CAN'T from available_tas
        
                
            #Collect all the skill documents and calculate their rarity
            skill_rarity, all_skill_docs = User.skill_rankings(self)
            
            #Sorts the available TAs according to skill_rarity, first in list = lowest uniquness
            sorted_tas = User.ta_scores(self, available_tas, all_skill_docs, skill_rarity)
            
            #Select the TA with the lowest uniqueness score
            best_ta = sorted_tas[0][0] if sorted_tas else None
            
            
            #This document needs to be stored in the shifts collection all docs with a pending status
            #All docs with a pending status send to admin pannel 
            
            shift_doc = {
                "_id": uuid.uuid4().hex,
                "ta_id": best_ta,
                "ml_id": ml_id,
                "date": requested_date,
                "start_time": start_time_iso,
                "end_time": end_time_iso,
                "room": room,
                "building": building_id,
                "floor": floor,
                "description": description,
                "skills": skills,
                "status": "pending"  #Could be: "pending", "approved", "rejected", "assigned", "completed"
            }
        
        #Automatic mode, no Admin approval needed
        elif operation_mode == 5:
            
            print("Running Operation Mode 5")


        #print("User List for each skill:", user_sets)
        #print("Users who have all the skills:", ta_candidates)
        #print("TA availability docs:", ta_availability_docs)
        #print("Available TAs with matching skill set and availability:", available_tas)
        #print("All skill docs:", all_skill_docs)
        #print("Skill Counts:", skill_counts)
        #print("Skill Rarity:", skill_rarity)
        
        #print("Sorted TAs:", sorted_tas)
        #print("Most Suitable TA:", best_ta)
        #print("Module Leader _id:", ml_id)
        #print("Shift Doc:", shift_doc)
        
        return jsonify (operation_mode)
        return jsonify(success=True, message="Form Data sent successfully HELLLO")
    
    
        
        
        
        
    
        

    

        
        
        
        
        
        
        
    



        
    
    
 
        
        
        