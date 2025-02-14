from flask import Flask, render_template
import pymongo

#Create an instance of the app
app = Flask(__name__)

#Secret key needed for sessions
app.secret_key = b"\x1a\xe2\xf9\x01K8'\xa7\x8c\x12\xddS\x88\x80R\xe1"

#Database
client = pymongo.MongoClient("localhost", 27017)
db = client.TAS


#Routes
from user import routes

#Route to home
@app.route('/')
def home():
    return render_template('login.html')

#Route to the dashboard, having the second / means theres only one route users can access
@app.route('/ta/')
def ta():
    return render_template('ta.html')

@app.route('/ml/')
def ml():
    return render_template('ml.html')

@app.route('/admin/')
def admin():
    return render_template('admin.html')





