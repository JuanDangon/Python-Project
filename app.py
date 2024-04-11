from flask import Flask, redirect, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instagram.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    follows_count = db.Column(db.Integer)  # Number of people the user follows
    followers_count = db.Column(db.Integer)  # Number of followers
    posts = db.relationship('Post', backref='user', lazy=True)  # User's posts

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.Text, nullable=True)  # Not all posts have captions
    media_url = db.Column(db.String(255), nullable=False)  # URL to the image/video
    likes_count = db.Column(db.Integer, default=0)  # Number of likes for the post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        password=data['password']  # Remember to hash the password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user_data = {
            'username': user.username,
            'followers': [follower.id for follower in user.followers],
            'posts': [{'id': post.id, 'content': post.content} for post in user.posts]
        }
        return jsonify(user_data)
    else:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/login/instagram')
def instagram_login():
    instagram_auth_url = 'https://api.instagram.com/oauth/authorize'
    params = {
        'client_id': 'your-instagram-app-id',
        'redirect_uri': 'your-redirect-uri',
        'scope': 'user_profile,user_media',
        'response_type': 'code'
    }
    url = f"{instagram_auth_url}?client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&scope={params['scope']}&response_type={params['response_type']}"
    return redirect(url)

@app.route('/auth/')
def instagram_auth():
    code = request.args.get('code')
    if code:
        access_token = exchange_code_for_token(code)
        
        return jsonify({'access_token': access_token})
    else:
        return 'Authorization failed.', 400

def exchange_code_for_token(code):
    url = 'https://api.instagram.com/oauth/access_token'

    # THIS PLACEHOLDER CODE NEEDS TO BE FIXED
    data = {
        'client_id': 'your-instagram-app-id',
        'client_secret': 'your-instagram-app-secret',
        'grant_type': 'authorization_code',
        'redirect_uri': 'your-redirect-uri',
        'code': code
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None


#Get access token and username
def fetch_user_info_and_posts(username, access_token):
    # Specify the fields to fetch from the Instagram API
    fields = 'username,follows_count,media{caption,media_url,like_count}'
    # Constructs the endpoint URL with the desired fields and the access token
    endpoint = f"https://graph.facebook.com/v12.0/{username}?fields={fields}&access_token={access_token}"
    
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def store_user_info_and_posts(user_data):
    user = User.query.filter_by(username=user_data['username']).first()
    if not user:
        user = User(username=user_data['username'])
        db.session.add(user)
        db.session.commit()
    
    for media in user_data['media']['data']:
        post = Post(
            caption=media.get('caption'),
            media_url=media['media_url'],
            likes_count=media.get('like_count', 0),  # Use .get() to provide a default value of 0 if 'like_count' is missing
            user_id=user.id
        )
        db.session.add(post)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure all tables are created
        user_data = fetch_user_info_and_posts('some_username', 'your_access_token') # Need
        if user_data:
            store_user_info_and_posts(user_data)
        #add_dummy_data()  # Add dummy data
    app.run(debug=True)



"""from flask import Flask, render_template, request
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
    app.run(debug = True)"""