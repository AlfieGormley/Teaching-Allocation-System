from flask import Flask, jsonify, request, session
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:

    
    #Pass in self and a user object as parameters
    def start_session(self, user):
        
        #Removes the password from the session
        del user['password']
        
        #Flag that a user is logged in
        session['logged in'] = True
        
        #Stores the user dictionary inside of the session
        session['user'] = user
        
        #Return the succesful status to the front end:
        return jsonify(user), 200
    
    
    #self refers to an instance of the class
    def register(self):
        print(request.form)
        
        #Creates a new user object from data collected from the html form
        user = {
            "_id": uuid.uuid4().hex,            #Generates a random unique identifier converted to a hex string
            "name": request.form.get("name"),   
            "email": request.form.get("email"), 
            "role": request.form.get("role"),   
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
            "email": request.form.get('email')
        })
        
        if user:
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid Login Credentials" }), 401