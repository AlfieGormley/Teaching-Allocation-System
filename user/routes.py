from flask import Flask
from app import app #From the app file import app
from user.models import User #Imports the user class into our routes file 

#At this url the register() method of the User() class is called
#Only POST methods are allowed
@app.route('/user/register', methods=['POST'])
def register():
    #Creates an instance of the User class from models.py and calls the register method
    return User().register()