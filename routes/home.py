from flask import Blueprint, render_template, session
import mysql.connector
from mysql.connector import Error
from config import db_config

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    user = session.get('user')
    if user:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT name FROM students_profile WHERE email = %s', (user,))
            profile = cursor.fetchone()
            conn.close()
            if profile:
                return render_template('index.html', user=profile['name'].split()[0])
            else:
                print("User profile not found.")
        except Error as e:
            print(f"Database error: {e}")
    return render_template('index.html', user=None)