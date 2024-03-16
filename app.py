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
            birthDate = request.form('DOB')

            if phoneNumber > 9999999999 or phoneNumber < 0:
                msg = "Invalid phone number."
                return render_template('signup.html')
            
            if email[-4:] != ".com":
                msg = "Invlaid email address."
                return render_template('signup.html')
            
            for i in email:
                if i == "@":
                    goodEmail = 1

            if goodEmail == 0:
                msg = "Invlaid email address."
                return render_template('signup.html')

            with sqlite3.connect("SiteData.db") as con:        
                cur = con.cursor()
                
                cur.execute("SELECT * FROM Users WHERE Username = ?", (username,))
                sameUsername = cur.fetchall
                if sameUsername: 
                    msg = "This username is already in use."
                    return render_template('signup.html')

        except: 
            con.rollback()
            msg = "error in insert operation"

    else:
        return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug = True)