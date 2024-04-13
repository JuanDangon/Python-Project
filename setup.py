import sqlite3


def setup():
    user_table_statement = """CREATE TABLE IF NOT EXISTS Users (
                            UserId INTEGER PRIMARY KEY,
                            Username TEXT,
                            Password TEXT,
                            FirstName TEXT,
                            LastName TEXT,
                            DOB TEXT,
                            Email TEXT,
                            PhoneNumber TEXT"""

    conn = sqlite3.connect('userData.db')

    cursor = conn.cursor()
    cursor.execute(user_table_statement)
    # Do whatever Table Creation Here

    conn.commit()
    conn.close()