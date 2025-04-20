from typing import Self
from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
from datetime import datetime
from datetime import timedelta, timezone
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
            "password": request.form.get("password"), 
            "max_weekly_hours": request.form.get("max_hours")
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
        
        # Helper function to check if the time is already a datetime object
        def localize_if_needed(time, requested_date=None):
            if isinstance(time, datetime):  # If it's already a datetime object
                # If the datetime is naive (no timezone), localize it to UTC
                return time if time.tzinfo else timezone.localize(time)
            else:  # If it's a string (in your case, in the format "YYYY-MM-DD HH:MM")
                # Parse the string into a datetime object and localize to UTC
                return timezone.localize(datetime.strptime(f"{requested_date} {time}", "%Y-%m-%d %H:%M"))

        # Check and convert start_time
        if isinstance(start_time, datetime):  # If it's already a datetime object
            start_time_iso = localize_if_needed(start_time)
        else:
            start_time_iso = localize_if_needed(start_time, requested_date)

        # Check and convert end_time
        if isinstance(end_time, datetime):  # If it's already a datetime object
            end_time_iso = localize_if_needed(end_time)
        else:
            end_time_iso = localize_if_needed(end_time, requested_date)
        
        #Convert to ISODate Format
        #start_time_iso = datetime.strptime(f"{requested_date} {start_time}", "%Y-%m-%d %H:%M")
        #end_time_iso = datetime.strptime(f"{requested_date} {end_time}", "%Y-%m-%d %H:%M")
        
        #Localise with the time zone
        #start_time_iso = timezone.localize(start_time_iso)
        #end_time_iso = timezone.localize(end_time_iso)
        
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
    
    
    #Calculates the commute time between "approved" and "pending" shift
    def calculate_commute_time(self, scheduled_building, building, scheduled_floor, floor):
        
        #Floor travel time in seconds
        #THINK ABOUT MORE:
        floor_travel_time = 0.5 #(30 seconds per floor)
        
        #Convert floor to integer
        floor = int(floor)
        
        #Check if buildings are different
        if scheduled_building != building:
            print("Calculating Commute Time!")
                    
            #Collect travel time record between buildings
            travel_time_record = db.travel_times.find_one(
                {"building_a": scheduled_building, "building_b": building}
            )

            #Extract travel_time from record
            travel_time = travel_time_record["travel_time"]
                    
            print("Travel Time: ", travel_time) #Debugging
            
            #Calculate Floor Commute Time
            floor_commute = (scheduled_floor + floor) * floor_travel_time
                    
            #Calculate Commute time
            commute_time = floor_commute + travel_time
            
            return commute_time
            
            
        #Condition triggered when shifts occur in the same building
        else:
            
            print("Calculating Commute Time Between Floors")
            
            #Store commute time between floors
            commute_time = abs(scheduled_floor - floor) * floor_travel_time
            
            return commute_time
        
        
        
    def to_datetime_if_needed(time, date):
        if isinstance(time, datetime):
            return time
        combined = f"{date} {time}"
        dt = datetime.strptime(combined, "%Y-%m-%d %H:%M")
        #dt = pytz.UTC.localize(dt)
        return dt
    

    
    
    
    
    
    
    #We have checked if a TA will be able to make this new reuested shift from their previously scheudled shift
    #We must also check the case where a TA wont be able to make it to an exisiting shift if they take the requested shift
    
    #Need to add check for max hours
    
    #Returns eligible TAs whose schedule allows time to commute  
    def filter_available_tas(self, floor, start_time, available_tas, date, building, end_time):
        
        #Convert if neccessary
        start_time = User.to_datetime_if_needed(start_time, date)
        end_time = User.to_datetime_if_needed(end_time, date)
        
        #List to store eligible_tas
        eligible_tas = []
        
        #Loop through each available TA
        for ta in available_tas:
            
            #Collect shift records for this TA on the same date
            shift_records = list(db.shifts.find({"ta_id": ta, "date": date, "status": "approved"}))
            
            #No shifts -> TA is available
            if not shift_records:
                eligible_tas.append(ta)
                continue  # No need to check further
            
            # Check if any scheduled shift prevents TA from taking the new one
            available = True
            for shift in shift_records:
                
                print("Shift:", shift) #Debugging
                
                #Extract shift data for calculate_commute_time()
                scheduled_floor = int(shift["floor"])
                scheduled_building = shift["building"]
                
                #Extract end time of "approved" shift
                scheduled_end_time = shift["end_time"]
                scheduled_start_time = shift["start_time"]
                
                #Calculate Commute Time
                commute_time = User.calculate_commute_time(Self, scheduled_building, building, scheduled_floor, floor)
                print("Commute Time:", commute_time) #Debugging
                
                # Convert commute_time to timedelta
                commute_duration = timedelta(seconds=commute_time)
                
                #If the TA can make it from the scheudled shift factoring commute time
                if scheduled_end_time + commute_duration <= start_time:
                    print("TA can make the shift")
                    
            
                #If the TA can't make it factoring commute time
                else:
                    print("TA can't make the shift")
                    #Make available false which means ta wont be eligible
                    available = False
                    
                    
                #Check for timing overlaps
                if not (start_time >= scheduled_end_time or (end_time + commute_duration) <= scheduled_start_time):
                    print("Time overlap detected! TA has another scheduled shift.")
                    available = False
                    


            #If TA eligible add to list
            if available == True:
                eligible_tas.append(ta) 
            else:
                continue
                    
        return eligible_tas
    
    
    #Assigns TA, status = "approved" for given shift_id
    def approve_and_assign_ta(self, shift_id, ta_id, status):
        
        #Search shift_id and update relevent fields
        db.shifts.update_one(
            {"_id": shift_id},  
            {"$set": {"ta_id": ta_id, "status": "approved"}}
        )
        
        if status == "pending":
            #Adjust the Queue
            print("Adjusting queue")
            User.adjust_queue()
        
    
        return print(f"Shift {shift_id} has been assigned to TA {ta_id} and approved.")
    
    
    def get_week_boundary(start_time):
        
        # Ensure datetime is in UTC and reset time to 00:00:00
        start_time = start_time.astimezone(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        #Calculate Monday of the same week
        start_of_week = start_time - timedelta(days=start_time.weekday())
        
        #End of week: Sunday at 23:59:59.999999
        end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)
        
        return start_of_week, end_of_week
        
    
    
    def hour_checker(eligible_tas, start_time, end_time):
        
        still_eligible = []
        
        #Calculate boundary
        start_of_week, end_of_week = User.get_week_boundary(start_time)
        
        print("Monday:", start_of_week)
        print("Sunday:", end_of_week )
        
        #Start of week and end of week should be iso dates like in the database datetime.datetime localised
        
        
        #Calculate the duration of the new shift in hours
        new_shift_duration = (end_time - start_time).total_seconds() / 3600

        #Do this for each eligible_ta:
        for ta_id in eligible_tas:
            
            print("Assessing:", ta_id)
            
            user = db.users.find_one({ "_id": ta_id })
        
            if user:
                
                #Collect that users max weekly hours:
                max_weekly_hours = float(user.get('max_weekly_hours'))
                
                print(f"Max Weekly Hours : {max_weekly_hours}")
                
                
            
                weekly_shifts = db.shifts.find({
                    "ta_id": ta_id,
                    "status": "approved",
                    "start_time": { "$gte": start_of_week, "$lte": end_of_week }
                })
                
                print("Weekly Shifts", weekly_shifts)

                total_weekly_hours = 0.0
                for shift in weekly_shifts:
                    shift_start = shift["start_time"]
                    shift_end = shift["end_time"]

                    # Calculate shift duration
                    duration_hours = (shift_end - shift_start).total_seconds() / 3600
                    print("Duration Hours:", duration_hours)
                    total_weekly_hours += duration_hours
                    
                print("total_weekly_hours type:", type(total_weekly_hours))
                print("max_weekly_hours type:", type(max_weekly_hours))
                print("new_shift_duration type:", type(new_shift_duration))
                
                print("total_weekly_hours :", total_weekly_hours)
                print("max_weekly_hours :", max_weekly_hours)
                print("new_shift_duration :", new_shift_duration)
                
            # Check if adding this new shift would exceed their max
            if total_weekly_hours + new_shift_duration <= max_weekly_hours:
                still_eligible.append(ta_id)
            else:
                print("TA exceeds weekly limit – skipping.")

            
        return still_eligible
    
    #Considerations, if we cancel a pending shift we have to adjust the queue
    #We need to remove cancelled shifts from the form and not display them
    def cancel_shift():
        
        form_data = request.form
        print("Data from form:", form_data)
        _id = request.form.get('_id')
        print("ID:", _id)
        
        shift = db.shifts.find_one({ "_id": _id })
        
        if shift:
            status = shift.get('status')
            print(f"Shift status: {status}")
        else:
            print("Shift not found.")
        
        if status == "pending":
            #Adjust the Queue
            print("Adjusting queue")
            User.adjust_queue()
            
        #Set status to "cancelled"
        db.shifts.update_one(
            {"_id": _id},  
            {"$set": {"status": "cancelled"}}
        )
    
        
        return jsonify({"message": "Shift cancelled successfully"}), 200
        
    def deny_request(self, shift_id, status):
        
        #When a shift is rejected due to having no eligigble TAs its status is "queued"
        #We should still adjust the queue
        print("Status before the rejection:", status)
        
        
        #Search shift_id and update relevent fields
        db.shifts.update_one(
            {"_id": shift_id},  
            {"$set": {"status": "rejected"}}
        )
    
        
        shift = db.shifts.find_one({ "_id": shift_id })
        
        if shift:
            test_shift_status = shift.get('status')
            print(f"Shift status of rejected shift: {test_shift_status}")
        else:
            print("Shift not found.")
        
        #Here the status is rejected
        
        #Adjust the Queue
        if status == "pending":
            #Adjust the Queue
            print("Adjusting queue")
            User.adjust_queue()
            
        
            
        print(f"Shift {shift_id} has been rejected.") 
        
        return test_shift_status
    
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
                "active": True,
                "description": ""
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
                "active": True,
                "description": ""
            })
        

        return jsonify(success=True, message=f"Operation mode {operation_mode} is now active")
    
    
    def request_support(self):
        
        #Collect Module Leader _id from the session
        ml_id = session.get('user').get('_id')
        
        #Collect the currently active operation mode document
        active_mode_doc = db.operation_mode.find_one({"active": True})
        
        #Assign operation mode
        operation_mode = int(active_mode_doc["operation_mode"])
        
        #Extract data from the request form
        requested_date, skills, start_time, end_time, building_id, floor, room, description = User.exctract_request_form(self)
        
        #Convert start and end time
        start_time_iso , end_time_iso = User.convert_to_iso(self, requested_date, start_time, end_time)
        
        #Modes which require queue system
        queue_required_modes = [1, 4] 
        
        #Determine if active operation mode requires a queue
        is_queued_mode = operation_mode in queue_required_modes
        
        #if a queue is needed
        if is_queued_mode:
            # Get queue position (count shifts in queue)
            queue_position = db.shifts.count_documents({"status": {"$in": ["pending", "queued"]}}) 
            status = "pending" if queue_position == 0 else "queued"
        else:
            status = "pending"
            
        #BUILD THIS INTO EACH FUNCTION AND GIVE THE ADMIN AN OPTION TO DISABLE IT
        #If room is on the ground floor:
        if floor == "G":
            print("Searching for Disbaled TAs With Suitable Availability")
            
            #Collect TAs with mobility issues matching the desired skill set
            ta_candidates = User.get_disabled_ta_candidates(self, skills)
            
            #Get TAs who have the desired skill set with mobility issues
            return print("Disabled Candidates:", ta_candidates)
        
    
        #Mode to randomise TA selection out of the eligible TAs matching the skill set Admin sees TA before approval
        elif operation_mode == 1:
            
            #Call operation mode 1
            print("Running Operation Mode 1")
            best_ta, status, shift_id = User.operation_mode_1(skills, start_time, end_time, floor, requested_date, building_id, "Not Yet Assigned", status)
            
        
        #Mode in which admin grants approval pre TA allocation ✅
        elif operation_mode == 2:
            print("Running Operation Mode 2")
            best_ta = "Not Yet Assigned"
            shift_id = uuid.uuid4().hex
            
        #Mode in which admin can select candidate based on a specific quota (TA information will have to be displayed)
        elif operation_mode == 3:
            print("Running Operation Mode 3") 
        
        #Mode in which admin grants approval post TA allocation (Much slower, queue needed must be done one at a time)
        elif operation_mode == 4:
            print("Running Operation Mode 4")
            #Call operation mode 4
            best_ta, status, shift_id = User.operation_mode_4(skills, start_time, end_time, floor, requested_date, building_id, "Not Yet Assigned", status)
           
        #Automatic mode, no Admin approval needed
        elif operation_mode == 5:
            print("Running Operation Mode 5")

        #Create shift document
        shift_doc = {
                "_id": shift_id,
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
                "operation_mode": operation_mode,
                "status": status,
                "queue_position": queue_position if is_queued_mode else None  
            }
        
        #Store the document in the shifts collection
        db.shifts.insert_one(shift_doc)

        return jsonify(success=True, message="Shift request added.")
        
    
    #Make this method handle all the modes of operation
    def manage_pending_shift():
        
        #Collect action "approve/deny"
        action = request.form.get("action")
        print("Action:", action) #Debugging
        
        #Collect shift_ids
        shift_ids = request.form.getlist("shift_ids")
        print("Shift_ids:", shift_ids) #Debugging
        
        #Collect Relevant Shift Documents
        shift_docs = list(db.shifts.find({"_id": {"$in": [shift_id for shift_id in shift_ids]}}))

        #Loop Through Shift Documents
        for shift_doc in shift_docs:
            print("Processing shift:", shift_doc)
            
            #Process Shift Info
            shift_info = {
                "shift_id": shift_doc["_id"],  
                "ta_id": shift_doc["ta_id"],
                "module_leader_id": shift_doc["ml_id"],
                "date": shift_doc["date"],
                "start_time": shift_doc["start_time"], 
                "end_time": shift_doc["end_time"],
                "room": shift_doc["room"],
                "building_id": shift_doc["building"],
                "floor": shift_doc["floor"],
                "description": shift_doc["description"],
                "skills": shift_doc["skills"], 
                "operation_mode": shift_doc["operation_mode"],
                "status": shift_doc["status"],
            }
            
            if action == "approve" and shift_info["operation_mode"] == 1:
                
                #Assigns TA and approves the shift
                print("Approving Shift and Assigning TA")
                User.approve_and_assign_ta(Self, shift_info["shift_id"], shift_info["ta_id"], shift_info["status"])
                
                
            
            elif action == "approve" and shift_info["operation_mode"] == 2:

                User.operation_mode_2(shift_info["skills"], shift_info["start_time"], shift_info["end_time"], shift_info["floor"], shift_info["date"], shift_info["building_id"], shift_info["shift_id"], shift_info["status"])
            
            elif action == "approve" and shift_info["operation_mode"] == 3:
                print("Running Operation Mode 3")
            
            elif action == "approve" and shift_info["operation_mode"] == 4:
                
                #Assigns TA and approves the shift
                print("Approving Shift and Assigning TA")
                User.approve_and_assign_ta(Self, shift_info["shift_id"], shift_info["ta_id"], shift_info["status"])
            
                
            
            elif action == "approve" and shift_info["operation_mode"] == 5:
                print("Running Operation Mode 5")
                
            elif action == "deny":
                print("Rejecting Request")
        
                #Sets status to rejected
                User.deny_request(Self, shift_info["shift_id"])
                
        return jsonify("Form Data Recived:", action)
    
    
    def change_operation_mode():
        
        form_data = request.form
        
        operation_mode_id = next(iter(form_data))
        
        print("Extracted ID:", operation_mode_id)
        
        db.operation_mode.update_many({}, {"$set": {"active": False}})
        
        db.operation_mode.update_one(
            {"_id": operation_mode_id},
            {"$set": {"active": True}}
        )
        
        return jsonify("Form Data Recived:")
    
    
    
    def eligible_tas(skills, start_time, end_time, floor, date, building_id):
        
        start_time_iso , end_time_iso = User.convert_to_iso(Self, date, start_time, end_time)
        
        if floor == "G":
            
            #Collect TAs with mobility issues matching the desired skill set
            ta_candidates = User.get_disabled_ta_candidates(Self, skills)
            
            if not ta_candidates:
                ta_candidates = User().get_ta_candiates(skills)
                
            
        else:
            #Get TAs who have the desired skill set
            ta_candidates = User().get_ta_candiates(skills)
            
        #Collect ta_candidates with matching availablility
        available_tas = User.get_available_tas(Self, ta_candidates, start_time_iso, end_time_iso)
        print("Available_TAS:", available_tas)
                
        #Out of these TAs who can make it factoring commute time 
        eligible_tas = User.filter_available_tas(Self, floor, start_time, available_tas, date, building_id, end_time)
        print("Eligible_TAS:", eligible_tas)
        
        still_eligible = User.hour_checker(eligible_tas, start_time_iso, end_time_iso)
        
        
            
        return still_eligible
    
    
    
    
    #Select random TA from eligible TAs, Admin must view TA before approval
    #Function for approving/denying shifts in operation mode 1
    def operation_mode_1(skills, start_time, end_time, floor, date, building_id, shift_id, status):
        
        if shift_id == "Not Yet Assigned":
            print("Shift ID is not yet assigned")
            shift_id = uuid.uuid4().hex
            print("Shift_id:", shift_id)
        
        print("Processing shift id:", shift_id)
        
        shift_doc = db.shifts.find_one({"_id": shift_id}, {"queue_position": 1})
        
        if shift_doc and "queue_position" in shift_doc:
            queue_position = shift_doc["queue_position"]
            print("Queue Position:", queue_position, "For shift:", shift_id)
        else:
            print("Shift not found or queue_position missing.")
            queue_position = 0
            
        
        #Check if status is pending
        if status == "pending":
        
            eligible_tas = User.eligible_tas(skills, start_time, end_time, floor, date, building_id)
                
            #Randomly select a candidate
            best_ta = random.choice(eligible_tas)
                
            
        elif status == "queued" and queue_position == 1:
            
            #Shift has been queued waiting for admin to accept approve a "pending" shift
            print("Processing shift at the front of the queue")
            
            eligible_tas = User.eligible_tas(skills, start_time, end_time, floor, date, building_id)
            
            #Randomly select a candidate
            best_ta = random.choice(eligible_tas) 
            
        #Shift has been queued waiting for admin to accept approve a "pending" shift
        else:
            #Shift at front of queue, process and set status to "pending"
            print("Shift is queued")
            
            #Can't calculate the best TA yet
            best_ta = "Not Yet Assigned"
            
        return best_ta, status, shift_id
    
    #Mode in which admin grants approval pre TA allocation ✅
    #Function for approving/denying shifts in operation mode 2
    def operation_mode_2(skills, start_time, end_time, floor, date, building_id, shift_id, status):
        
        eligible_tas = User.eligible_tas(skills, start_time, end_time, floor, date, building_id)
                
        #Calculates the rarity of each skill in a ranking system
        skill_rarity, all_skill_docs = User.skill_rankings(Self)
                    
        #Sorts the eligible TAs according to skill_rarity, first in list = lowest uniquness
        sorted_tas = User.ta_scores(Self, eligible_tas, all_skill_docs, skill_rarity)
                
        #If there are candidates in the list
        if sorted_tas:
            #Select the TA with the lowest uniqueness score
            best_ta = sorted_tas[0][0]
                    
            #Assigns TA and approves the shift
            User.approve_and_assign_ta(Self, shift_id, best_ta, status)
                    
        #sorted_tas is empty --> no suitable TAS
        else:
            #Sets status to rejected
            User.deny_request(Self, shift_id, status)
    
    #Mode in which admin can select candidate based on a specific quota (TA information will have to be displayed)
    def operation_mode_3():
        
        return
    
    
    #Mode in which admin grants approval post TA allocation (Much slower, queue needed must be done one at a time)
    #Function for approving/denying shifts in operation mode 4
    
    #Change this to 3 everywhere
    
    def operation_mode_4(skills, start_time, end_time, floor, date, building_id, shift_id, status):
        
        if shift_id == "Not Yet Assigned":
            print("Shift ID is not yet assigned")
            shift_id = uuid.uuid4().hex
            print("Shift_id:", shift_id)
        
        
        print("Processing shift id:", shift_id)
        
        shift_doc = db.shifts.find_one({"_id": shift_id}, {"queue_position": 1})
        
        if shift_doc and "queue_position" in shift_doc:
            queue_position = shift_doc["queue_position"]
            print("Queue Position:", queue_position, "For shift:", shift_id)
        else:
            print("Shift not found or queue_position missing.")
            queue_position = 0
        
        
        
        #Check if status is pending
        if status == "pending":
            
            eligible_tas = User.eligible_tas(skills, start_time, end_time, floor, date, building_id)
            
            #Hadle being empty
            if not eligible_tas:
                
                #Reject the shift
                User.deny_request(Self, shift_id, status)
                
                
                best_ta = "Could Not be Assigned"
                print("Status ff the shift the just got rejected:", status)
                
                
                return best_ta, status, shift_id
                
            
            
            #Collect all the skill documents and calculate their rarity
            skill_rarity, all_skill_docs = User.skill_rankings(Self)
                
            #Sorts the available TAs according to skill_rarity, first in list = lowest uniquness
            sorted_tas = User.ta_scores(Self, eligible_tas, all_skill_docs, skill_rarity)
            
            print("Sorted_TAS:", sorted_tas)
                
            #Select the TA with the lowest uniqueness score
            best_ta = sorted_tas[0][0] if sorted_tas else None
            
            
        #Currently the shift first in the queue is entering this statement which is wrong   
        # Maybe lookup the queue position of the shift, if it is 1 then its at the front     
            
        elif status == "queued" and queue_position == 1:
            
            #Shift has been queued waiting for admin to accept approve a "pending" shift
            print("Processing shift at the front of the queue")
            
            eligible_tas = User.eligible_tas(skills, start_time, end_time, floor, date, building_id)
            
            #Hadle being empty
            if not eligible_tas:
                
                #Reject the shift
                test_shift_status = User.deny_request(Self, shift_id, status)
                
                best_ta = "Could Not be Assigned"
                
                
                
                
                
                
                
                #Here the status is queued
                print("Status of the shift that just got rejected:", test_shift_status )
                
                return best_ta, status, shift_id
            
            #Collect all the skill documents and calculate their rarity
            skill_rarity, all_skill_docs = User.skill_rankings(Self)
                
            #Sorts the available TAs according to skill_rarity, first in list = lowest uniquness
            sorted_tas = User.ta_scores(Self, eligible_tas, all_skill_docs, skill_rarity)
                
            #Select the TA with the lowest uniqueness score
            best_ta = sorted_tas[0][0] if sorted_tas else None
            
            print("Best TA:", best_ta)
            
            
        #Shift has been queued waiting for admin to accept approve a "pending" shift
        else:
            #Shift at front of queue, process and set status to "pending"
            print("Shift is queued")
            
            #Can't calculate the best TA yet
            best_ta = "Not Yet Assigned"
            
            
        print("Shift ID:", shift_id)
        print("Best TA:", best_ta)
            
        return best_ta, status, shift_id
    
    #Automatic mode, no Admin approval needed
    def operation_mode_5():
        
        return
    
    #Once this is working properly we can then finish the logic for each operation mode
    #We dont need to handle operation modes where the TA is not shown before approval
    
    #This needs to handle cases where a shift has been rejected
    def adjust_queue():
        
        #The shift with queue position 1 is the next shift to be processed
        
        #Collect all shifts with status "queued"
        shift_queue = list(db.shifts.find({"status": "queued"}))
        
        print("Queued Shifts:", shift_queue)
        
        for shift in shift_queue:
            #Collect queue position
            queue_position = shift['queue_position']
            
            print("Queue Position:", queue_position)
            
            #Calculate new queue position
            new_queue_position = queue_position - 1
            
            #We are checking if the shift is at the front of the queue, its been rejected but its still at the front so it will be processed  
            
            #If the current shift is at the front of the queue
            if queue_position == 1:

                #Check its operation mode
                print("Checking Operation Mode")
            
                print("Processing shift at the front of the queue")
                
                #Call approprate operation mode 
                operation_mode = shift["operation_mode"]
                
                #Select random TA from eligible TAs, Admin must view TA before approval
                if operation_mode == 1:
                    print("Running Operation Mode 1")
                    #Call operation Mode 1
                    best_ta, status, shift_id = User.operation_mode_1(shift["skills"], shift["start_time"], shift["end_time"], shift["floor"], shift["date"], shift["building"], shift["_id"], shift["status"])
                    
        
                #Mode in which admin can select candidate based on a specific quota (TA information will have to be displayed)
                elif operation_mode == 3:
                    print("Running Operation Mode 3") 
        
                #Mode in which admin grants approval post TA allocation (Much slower, queue needed must be done one at a time)
                elif operation_mode == 4:
                    print("Running Operation Mode 4 in the queue adjustment phase")
                    #Call operation Mode 4
                    best_ta, status, shift_id = User.operation_mode_4(shift["skills"], shift["start_time"], shift["end_time"], shift["floor"], shift["date"], shift["building"], shift["_id"], shift["status"])
                    
                    
                #Automatic mode, no Admin approval needed
                elif operation_mode == 5:
                    print("Running Operation Mode 5")
                    
            
                print("Best TA Just Before Update", best_ta)
                
                #If best_ta is "Could Not be Assigned"
                if best_ta == "Could Not be Assigned":
                    db.shifts.update_one(
                    {"_id": shift["_id"]},
                    {"$set": {"queue_position": new_queue_position, "ta_id": best_ta}}
                    )
                    print("Didnt set its status to pending")
                
                else:
                    db.shifts.update_one(
                    {"_id": shift["_id"]},
                    {"$set": {"queue_position": new_queue_position, "status": "pending", "ta_id": best_ta}}
                    )
                
                
            #If the shift isnt at the front of the queue move it forward one position
            else:
                #Update queue position
                db.shifts.update_one(
                {"_id": shift["_id"]},
                {"$set": {"queue_position": new_queue_position}}
                )
            
    
        return print("Queue Adjusted")
    
    
    
        
        
        
        
        
        
      
    
    
    
    
    def get_user_shifts(user_id):
        
        #Collect relevent shift documents
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
        
        print(formatted_shifts)
        
        return formatted_shifts
    
    
    
            
        
    
        

    

        
        
        
        
        
        
        
    



        
    
    
 
        
        
        