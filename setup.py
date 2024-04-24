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

# Create Roles table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS roles (
        id INTEGER PRIMARY KEY,
        role_name TEXT UNIQUE
    )
''')

# Create Permissions table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS permissions (
        id INTEGER PRIMARY KEY,
        permission_name TEXT UNIQUE
    )
''')


# these are the permissions each role has 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS role_permissions (
        role_id INTEGER,
        permission_id INTEGER,
        FOREIGN KEY (role_id) REFERENCES roles(id),
        FOREIGN KEY (permission_id) REFERENCES permissions(id),
        PRIMARY KEY (role_id, permission_id)
    )
''')


# Insert roles into Roles table
cursor.execute("INSERT INTO roles (role_name) VALUES (?)", ('admin',))
cursor.execute("INSERT INTO roles (role_name) VALUES (?)", ('regUser',))
cursor.execute("INSERT INTO roles (role_name) VALUES (?)", ('premiumUser',))

# Insert permissions into Permissions table
cursor.execute("INSERT INTO permissions (permission_name) VALUES (?)", ('adminAccess',))
cursor.execute("INSERT INTO permissions (permission_name) VALUES (?)", ('regAccess',))
cursor.execute("INSERT INTO permissions (permission_name) VALUES (?)", ('premiumAccess',))

# Grant permissions to roles in RolePermissions table
cursor.execute("INSERT INTO role_permissions (role_id, permission_id) VALUES (?, ?)", (1, 1))  # Admin has adminAccess
cursor.execute("INSERT INTO role_permissions (role_id, permission_id) VALUES (?, ?)", (2, 2))  # RegUser has regAccess
cursor.execute("INSERT INTO role_permissions (role_id, permission_id) VALUES (?, ?)", (3, 3))  # PremiumUser has premiumAccess

# Insert an admin user
password_hash = generate_password_hash('password')  # Hash the password
cursor.execute('''
INSERT INTO user (username, password, role)
VALUES (?, ?, ?)
''', ('juanadmin', password_hash, 'admin'))

conn.commit()
conn.close()