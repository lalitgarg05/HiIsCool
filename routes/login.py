from flask import Blueprint, Flask, render_template, request, redirect, session, flash, jsonify
import mysql.connector
import bcrypt
import smtplib
import os
import base64
import json
from mysql.connector import Error
from config import db_config  # Ensure this is correctly configured
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config import db_config

login_bp = Blueprint('login', __name__)
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for sessions
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute('SELECT username, password FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()
            conn.close()

            if user:
                if check_password_hash(user[1], password):
                    session['user'] = username
                    flash(f'Welcome back, {username}!')
                    return redirect('/')
                else:
                    flash('Invalid username or password.')
            else:
                flash('Invalid username or password.')
        except Error as e:
            flash(f'Database error: {e}')
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.')
    return redirect('/login')

@login_bp.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    try:
        msg = MIMEText('You have successfully registered on HiIsCool. We are excited to have you on board!')
        msg['Subject'] = 'Welcome to HiIsCool.'
        msg['From'] = os.getenv('EMAIL_ADDRESS')
        msg['To'] = email

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        print(msg.as_string())

        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)
        message = {'raw': raw}

        try:
            message = (service.users().messages().send(userId='me', body=message).execute())
            return jsonify({'message': 'Email sent successfully!'}), 200
        except Exception as e:
            print(f"Failed to send email: {e}")
            return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Failed to create email: {e}")
        return jsonify({'error': str(e)}), 500

def get_credentials():
    creds = None
    token_path = 'token.json'
    creds_path = 'credentials.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return creds


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        hashed_password = generate_password_hash(password)

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (email, hashed_password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please log in.')
            return redirect('/login')
        except mysql.connector.IntegrityError:
            flash('Username already exists.')
        except Error as e:
            flash(f'Database error: {e}')
    return render_template('register.html')