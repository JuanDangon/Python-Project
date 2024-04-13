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
            SSN = request.form('ssn')

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
            
            if SSN > 999999999 or SSN < 0:
                msg = "Invalid SSN."
                return render_template('signup.html')
            
            if password != confirm:
                msg = "Passwords do not match"
                return render_template('signup.html')

            with sqlite3.connect("SiteData.db") as con:        
                cur = con.cursor()
                
                cur.execute("SELECT * FROM Users WHERE Username = ?", (username,))
                sameUsername = cur.fetchall
                if sameUsername: 
                    msg = "This username is already in use."
                    return render_template('signup.html')
                
                cur.execute("SELECT * FROM Users WHERE Email = ?", (email,))
                sameEmail = cur.fetchall
                if sameEmail: 
                    msg = "This Email is already in use."
                    return render_template('signup.html')
                
                cur.execute("SELECT * FROM Users WHERE SSN = ?", (SSN,))
                sameSSN = cur.fetchall
                if sameSSN: 
                    msg = "This SSN is already in use."
                    return render_template('signup.html')
                
                cur.execute("INSERT INTO Users (Username, Password, CreationDate, FirstName, LastName, Email, Phone, DOB, SSN) VALUES (?,?,?,?,?,?,?,?,?)", (username, password, time, firstName, lastName, email, phoneNumber, birthDate, SSN))

        except: 
            con.rollback()
            msg = "error in insert operation"

    else:
        return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
