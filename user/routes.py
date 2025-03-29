from flask import Flask, request, jsonify
from app import app #From the app file import app
from user.models import User #Imports the user class into our routes file 

#At this url the register() method of the User() class is called
#Only POST methods are allowed
@app.route('/user/register', methods=['POST'])
def register():
    #Creates an instance of the User class from models.py and calls the register method
    return User().register()


@app.route('/user/login', methods=['POST'])
def login():
    return User().login()


@app.route('/user/signout')
def signout():
    return User().signout()



@app.route('/user/update_skills', methods=['POST'])
def update_skills():
    return User().update_skills()


@app.route('/user/remove_skills', methods=['POST'])
def remove_skills():
    
    return User().remove_skills()



@app.route('/user/delete_user', methods=['POST'])
def delete_user():
    return User().delete_user()


@app.route('/user/change_password', methods=['POST'])
def change_password():
   return User().change_password()


@app.route('/user/toggle_mobile', methods=['POST'])
def toggle_mobile():
   #form_data = request.form.get("toggle")
   #print("Data from form:", form_data)
   
   #return jsonify(success=True, message="Skills updated successfully")
   return User().toggle_mobile()

@app.route('/user/set_availability', methods=['POST'])
def set_availability():
    return User().set_availability()

@app.route('/user/add_new_skill', methods=['POST'])
def add_new_skill():
    
    return User().add_new_skill()

@app.route('/user/admin_remove_skill', methods=['POST'])
def admin_remove_skill():
    
    return User().admin_remove_skill()


@app.route('/user/drop_availability', methods=['POST'])
def drop_availability():
    
    return User().drop_availability()

@app.route('/user/add_building', methods=['POST'])
def add_building():
    
    return User().add_building()

@app.route('/user/remove_building', methods=['POST'])
def remove_building():
    
    return User().remove_building()


@app.route('/user/set_travel_time', methods=['POST'])
def set_travel_time():
    
    return User().set_travel_time()

@app.route('/user/request_support', methods=['POST'])
def request_support():

    return User().request_support()

@app.route('/user/set_mode', methods=['POST'])
def set_operation_mode():
    
    return User.set_operation_mode()

@app.route('/user/manage_pending_shift', methods=['POST'])
def manage_pending_shift():
    
    #form_data = request.form
    #print("Data from form:", form_data)
    
    #action = request.form.get("action")
    
    #print("Action:", action)

    return User.manage_pending_shift()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   
   
    
   


    
    
    
    

    
    


