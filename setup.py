import sqlite3
import os
from werkzeug.security import generate_password_hash

# Create the instance directory if it doesn't exist
os.makedirs('instance', exist_ok=True)

conn = sqlite3.connect('instance/instagram.db')
cursor = conn.cursor()

# Create Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        usage_count INTEGER DEFAULT 0
    )
''')

# Create UserImage table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_image (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        image_type TEXT NOT NULL,
        image_path TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user (id)
    )
''')

# Insert an admin user
password_hash = generate_password_hash('password')  # Hash the password
cursor.execute('''
INSERT INTO user (username, password, role)
VALUES (?, ?, ?)
''', ('juanadmin', password_hash, 'admin'))

conn.commit()
conn.close()