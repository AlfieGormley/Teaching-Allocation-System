from flask import Flask, request
from app import app #From the app file import app
from user.models import User #Imports the user class into our routes file 

#At this url the register() method of the User() class is called
#Only POST methods are allowed
@app.route('/user/register', methods=['POST'])
def register():
    #Creates an instance of the User class from models.py and calls the register method
    return User().register()

#At this url the login() method of the User() class is called
@app.route('/user/login', methods=['POST'])
def login():
    #Creates an instance of the User class from models.py and calls the login method
    return User().login()

#At this url the signout() method of the User() class is called
@app.route('/user/signout')
def signout():
    #Creates an instance of the User class from models.py and calls the signout method
    return User().signout()



