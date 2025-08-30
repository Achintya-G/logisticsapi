import sqlite3
import jwt
import datetime
from flask import Flask, render_template, url_for, request, jsonify, redirect, session
import requests
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a strong secret!

DB_API_URL = "http://127.0.0.1:5001/" # THIS ONE IS VERY TEMPORARY CHANGE IT WHEN YOU FIGURE OUT HOSTING


# aight boss this one is lowkey ass but it does the job if yall can refer to the dbapi.py and structure this and make this better itll be good
# also the html pages are only for the purpose of testing when the actual api is there we wont need the renderhtml function to be returned
# yea the dbapi.py is simpler and easier to understand structure use that as a reference
# also i used sqlite3 when making but let that be for now we can change it later or talk to me if u changing it

def generate_token(username) -> str:
    payload = {
        'username': username,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=100)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    print(f"Generated token: {token}")
    return token


def verify_token(token) -> bool:
    print(f"Verifying token: {token}")
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return True
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False


def validate_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None
    

def register_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success



# 3 mains routes are here that actually have a webpage gotta remove these   

@app.route('/')
def home():
    username = session.get('username')
    return '''
    The following endpoints are accesible
    <ul>
    <li>/login [POST]</li>
    <li>/register [POST]</li>
    <li>/db</li>
    </ul>
    '''


@app.route('/login', methods=['POST'])
def login():
    '''
    Send a POST request with keys 'username' and 'password' in json body to recieve token
    '''
    if request.method == 'POST':

        username = request.json['username']
        password = request.json['password']

        if validate_user(username, password):
            data = {'token' : generate_token(username)}
            return data,200
        else:
            return {'error' : "Invalid credentials"},401
    else :
        return {'error' : "Invalid method"},405

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        '''
        Send a POST request with keys 'username' and 'password' in json body to register
        '''
        
        username = request.json['username']
        password = request.json['password']

        if register_user(username, password):
            return {'success': True, 'message': 'Registration successful'},200
        else:
            return {'success': False, 'message': 'Username already exists'},409
    else :
        return {'error' : "Invalid method"},405


#REMOVE GENTOKEN AND VERTOKEN AFTER DEV (these were for testing if the token thing works)

@app.route('/gentoken', methods=['POST']) ## the login api does the exact same thing now ill remove this later
def gentoken():
    for i in request.form.items(): 
        print(i)
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']


        print("usernaem:",username)
        print("password:",password)
        
        if validate_user(username, password):
            token = generate_token(username)
            return token , "\n this is your token."
    return "INVALID REQUEST"


@app.route('/vertoken', methods = ['POST'])
def vertoken():
    print("this is the header:\n",dict(request.headers))
    if request.method == 'POST':
        if verify_token(request.headers.get('authtoken')):
            return 'valid token'
    return 'sumn went wrong'


@app.route('/db', methods = ['GET','POST'])
def db_api_call():

    ## FINISH THE DB FUNCTIONS AND COME BACK TO THIS


    auth_token = request.headers.get('authtoken')
    
    if request.method == 'POST' and verify_token(auth_token) and request.is_json:
        print(type(request.json))
        print()
        return 'sumn data was recievd'
    
    return 'give authtoken'


if __name__ == "__main__":
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    app.run(port=5000,debug=True)

