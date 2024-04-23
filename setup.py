import sqlite3


# def setup():
user_table_statement = """CREATE TABLE IF NOT EXISTS Users(
                            UserID INTEGER PRIMARY KEY,
                            Username TEXT, 
                            Password TEXT,
                            CreationDate DATETIME,
                            FirstNam TEXT, 
                            LastName TEXT, 
                            Email TEXT, 
                            Phone INTEGER,
                            DOB DATETIME, 
                            SSN INTEGER)"""

account_info_statement = """CREATE TABLE IF NOT EXISTS AccountInfo(
                            Account INTEGER PRIMARY KEY,
                            AccessToken INTEGER,
                            FirstName TEXT,
                            LastName TEXT,
                            AccountName TEXT,
                            CreationDate DATETIME,
                            PostCount INTEGER,
                            FollowerCount INTEGER,
                            FollowingCount INTEGER,
                            """

conn = sqlite3.connect('userData.db')

try:
    cursor = conn.cursor()
    cursor.execute(user_table_statement)
    cursor.execute(account_info_statement)
except sqlite3.Error as e:
    print("Error while creating table:\n", e)
# Do whatever Table Creation Here

conn.commit()
conn.close()
