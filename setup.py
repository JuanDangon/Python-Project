import sqlite3

conn = sqlite3.connect('SiteData.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS Users (Username TEXT,Password TEXT,CreationDate DATETIME,FirstName TEXT,LastName TEXT, Email TEXT, Phone INTEGER, DOB DATETIME, SSN INTEGER)')

conn.commit()
conn.close()