import sqlite3

conn = sqlite3.connect('userData.db')
cursor = conn.cursor()

# Do whatever Table Creation Here

conn.commit()
conn.close()