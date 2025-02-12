from flask import Flask, render_template

#Create an instance of the app
app = Flask(__name__)

#Routes
from user import routes

#Route to home
@app.route('/')
def home():
    return render_template('home.html')

#Route to the dashboard, having the second / means theres only one route users can access
@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')





