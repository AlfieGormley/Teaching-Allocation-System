from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
import uuid

class User:
    
    def register(self):
        print(request.form)
        
        #Creating the user object
        user = {
            "_id": uuid.uuid4().hex,            #This will give a unique ID
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "role": request.form.get("role"),
            "password": request.form.get("password")
        }
        
        # Encrypting the passwords so they arent stored as plaintext in the database
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        
        #Returns user in a json format
        return jsonify(user), 200 