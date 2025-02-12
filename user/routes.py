from flask import Flask
from app import app #From the app file import app
from user.models import User #Imports the user class into our routes file 

@app.route('/user/register', methods=['POST'])
def register():
    return User().register()