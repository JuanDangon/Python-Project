from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#git test

if __name__ == '__main__':
    app.run(debug = True)