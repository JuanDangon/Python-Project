from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('signup.html', methods=['POST', 'GET'])
def addUser():
    con = None
    if request.method == 'POST':
        try: 
            time = datetime.now()
            username = request.form('Username')
            password = request.form('Password')
            confirm = request.form('Confirm')
            firstName = request.form('fName').title()
            lastName = request.form('lName').title()
            email = request.form('Email')
            phoneNumber = int(request.form('pNumber'))
            birthYear = int(str(request.form('DOB'))[:4])
            birthMonth = int(str(request.form('DOB'))[4:-2])
            birthDay = int(str(request.form('DOB'))[-2:])

        except: 
            con.rollback()
            msg = "error in insert operation"

    else:
        return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug = True)