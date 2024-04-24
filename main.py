import os
import base64
from datetime import datetime
from openai import OpenAI
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
client = OpenAI(api_key="sk-proj-XkFPt4pekFXuZvl8PHR0T3BlbkFJLiqQZctgDhe35fh2CUET")

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/instagram.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/juanmanueldangon/OpenAITest/instance/instagram.db'
app.config['SECRET_KEY'] = 'c8a5f9e1b8d4d3e9c3b1d8e1c8d1e9f1b8d4d3e9c3b1d8e1c8d1e9f1b8d4d3e9' # Set a secure secret key for session handling
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    usage_count = db.Column(db.Integer, default=0)
    images = db.relationship('UserImage', backref='user', lazy=True)

class UserImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_type = db.Column(db.String(20), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# Set up a temporary directory for storing uploaded images
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            if user.role == 'admin':
                return redirect('/admin')
            else:
                return redirect('/home')
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        role = 'basic'  # Default role for new users
        new_user = User(username=username, password=hashed_password, role=role)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except IntegrityError:
            db.session.rollback()
            error_message = "Username already exists. Please choose a different username."
            return render_template('signup.html', error=error_message)
        except SQLAlchemyError as e:
            db.session.rollback()
            error_message = str(e)
            return render_template('signup.html', error=error_message)
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

    
@app.route('/home')
def home():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    user = User.query.get(user_id)
    if user.role == 'basic':
        remaining_usage = 2 - user.usage_count
        return render_template('home.html', remaining_usage=remaining_usage, current_user=user)
    elif user.role == 'premium':
        remaining_usage = 10 # May want to limit this in the future
        return render_template('home.html', remaining_usage=remaining_usage, current_user=user)
    else:
        return render_template('home.html', current_user=user)

@app.route('/admin')
def admin():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    user = User.query.get(user_id)
    if user.role != 'admin':
        return redirect('/home', error='You must be an admin to access this page.')

    return render_template('admin.html')

@app.route('/admin/manage_users', methods=['GET', 'POST'])
def manage_users():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    admin_user = User.query.get(user_id)
    if admin_user.role != 'admin':
        return redirect('/home', error='You must be an admin to access this page.')

    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            if 'delete' in request.form:
                db.session.delete(user)
                db.session.commit()
            elif 'promote' in request.form:
                user.role = 'premium'
                db.session.commit()
        return redirect('/admin')
    return render_template('admin.html', user=None)

@app.route("/analyze", methods=["POST"])
def analyze():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    user = User.query.get(user_id)
    if user.role == 'basic' and user.usage_count >= 2:
        return "You have reached the maximum usage limit. Please upgrade to premium."

    # Retrieve the uploaded images from the form
    profile_image = request.files["profile_image"]
    post_images = request.files.getlist("post_images")

    # Save the images temporarily
    profile_image_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(profile_image.filename))
    profile_image.save(profile_image_path)

    post_image_paths = []
    for post_image in post_images:
        post_image_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(post_image.filename))
        post_image.save(post_image_path)
        post_image_paths.append(post_image_path)

    # Encode the images as base64
    profile_image_base64 = encode_image(profile_image_path)
    post_images_base64 = [encode_image(path) for path in post_image_paths]

    # Call the GPT-4 API to analyze the images and generate suggestions
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Give a short description of what each instagram post image contains. Then analyze the user's Instagram profile image and post images to provide suggestions for increasing engagement."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{profile_image_base64}"
                    }
                }
            ] + [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
                for base64_image in post_images_base64
            ]
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=300,
    )

    message_content = response.choices[0].message.content.strip()

    # Clean up the temporary images
    os.remove(profile_image_path)
    for post_image_path in post_image_paths:
        os.remove(post_image_path)

    user.usage_count += 1
    db.session.commit()

    return render_template('suggestions.html', suggestions=message_content)

@app.route('/analyze_stored', methods=['POST'])
def analyze_stored():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    user = User.query.get(user_id)
    if user.role != 'premium':
        return redirect('/home', error='You must be a premium user to use this feature.')

    # Retrieve the user's stored images from the database
    profile_image = UserImage.query.filter_by(user_id=user.id, image_type='profile').first()
    post_images = UserImage.query.filter_by(user_id=user.id, image_type='post').all()

    # Encode the stored images as base64
    profile_image_base64 = encode_image(profile_image.image_path) if profile_image else None
    post_images_base64 = [encode_image(post_image.image_path) for post_image in post_images]

    # Call the GPT-4 API to analyze the images and generate suggestions
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Give a short description of what each Instagram post image contains. Then analyze the user's Instagram profile image and post images to provide suggestions for increasing engagement."
                }
            ] + ([
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{profile_image_base64}"
                    }
                }
            ] if profile_image_base64 else []) + [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
                for base64_image in post_images_base64
            ]
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=300,
    )

    message_content = response.choices[0].message.content.strip()

    return render_template('suggestions.html', suggestions=message_content)

@app.route('/upgrade', methods=['GET', 'POST'])
def upgrade():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    user = User.query.get(user_id)

    if request.method == 'POST':
        # Perform payment processing logic here (dummy prompt for now)
        # If payment is successful, upgrade the user's role to 'premium'
        user.role = 'premium'
        db.session.commit()
        return redirect('/home')

    return render_template('upgrade.html', user=user)

@app.route('/premium', methods=['GET', 'POST'])
def premium():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    user = User.query.get(user_id)
    if user.role != 'premium':
        return redirect('/home', error='You must be a premium user to access this page.')

    if request.method == 'POST':
        if 'profile_image' in request.files:
            profile_image = request.files['profile_image']
            if profile_image:
                filename = secure_filename(profile_image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                profile_image.save(image_path)
                
                # Delete existing profile image if any
                existing_profile_image = UserImage.query.filter_by(user_id=user.id, image_type='profile').first()
                if existing_profile_image:
                    db.session.delete(existing_profile_image)
                    db.session.commit()
                
                # Add new profile image
                new_profile_image = UserImage(user_id=user.id, image_type='profile', image_path=image_path)
                db.session.add(new_profile_image)
                db.session.commit()

        if 'post_images' in request.files:
            post_images = request.files.getlist('post_images')
            for post_image in post_images:
                if post_image:
                    filename = secure_filename(post_image.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    post_image.save(image_path)
                    
                    # Add new post image
                    new_post_image = UserImage(user_id=user.id, image_type='post', image_path=image_path)
                    db.session.add(new_post_image)
                    db.session.commit()
            
            # Delete oldest post images if count exceeds 5
            post_images_count = UserImage.query.filter_by(user_id=user.id, image_type='post').count()
            if post_images_count > 5:
                oldest_post_images = UserImage.query.filter_by(user_id=user.id, image_type='post').order_by(UserImage.timestamp.asc()).limit(post_images_count - 5).all()
                for image in oldest_post_images:
                    db.session.delete(image)
                    db.session.commit()

    return render_template('premium.html', user=user)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)