from flask import Flask, render_template, request, redirect, session, flash, jsonify
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



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for sessions
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Home route
@app.route('/')
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
        
    # if 'user' in session:
    #     return render_template('index.html', user=session['user'])
    # return redirect('/login')

# Login route
@app.route('/login', methods=['GET', 'POST'])
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
                if bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):  # Assuming password is the second column in users table
                    session['user'] = username
                    #return redirect('/')
                    #@app.route('/')
                    #def home():
                    if 'user' in session:
                        return render_template('index.html', user=session['user'])
                    return redirect('/login')
                    flash(f'Welcome back, {username}!')
                    return redirect('/') #this line is basically taking u to a new page that has the session values from 2 lines before.
                else:
                    flash('Invalid username or password.')
            else:
                flash('Invalid username or password.')
        except Error as e:
            flash(f'Database error: {e}')
    return render_template('login.html')
    
# Jobs page
@app.route('/addNewJob')
def jobs():
    return render_template('postJobs.html')

# @app.route('/passcode')
# def passcode():
#     return render_template('passcode.html')

# Hiring page
@app.route('/jobs')
def hiring():
    return render_template('jobs.html')

# FAQ page
@app.route('/faq')
def faq():
    return render_template('faq.html')

# TOS page
@app.route('/terms')
def terms():
    return render_template('terms.html')

# Privacy page
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/contactUs')
def contact():
    return render_template('contactUs.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

# Add jobs route
# @app.route('/addjobs1', methods=['POST'])
# def addJobs1():
#     if 'user' not in session:
#         return redirect('/login')

#     try:
#         # Parse job details from the request body
#         # data = request.get_json()
#         # jobTitle = data.get('jobTitle')
#         # jobDescription = data.get('jobDescription')
#         # companyName = data.get('companyName')
#         # jobLocation = data.get('jobLocation')
#         # baseSalary = data.get('baseSalary')
#         jobTitle = request.form['jobTitle']
#         jobDescription = request.form['jobDescription']
#         companyName = request.form['companyName']
#         jobLocation = request.form['jobLocation']
#         baseSalary = request.form['baseSalary']
#         flash('XXXX ' + jobTitle)

#         # Validate input
#         # if not jobTitle or not jobDescription or not companyName or not jobLocation:
#         #     return jsonify({'error': 'All fields are required'}), 400

#         # Connect to the database and insert job
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor()
#         cursor.execute('''
#             INSERT INTO jobs (job_title, job_description, company_name, salary, job_location)
#             VALUES (%s, %s, %s, %s, %s)
#         ''', (jobTitle, jobDescription, companyName, baseSalary, jobLocation))
#         conn.commit()
#         conn.close()

#         return jsonify({'message': 'Job added successfully!'}), 201
#     except Error as e:
#         return jsonify({'error': f'Database error: {e}'}), 500
#     except Exception as e:
#         return jsonify({'error': f'Unexpected error: {e}'}), 500

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            return jsonify({'error': 'Request content type must be application/json'}), 400
        email = data.get('email')
        password = data.get('password')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

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
            #flash(f'Database error: {e}')
            flash(f'Database error: {e}')
    return render_template('register.html')

# Register route
@app.route('/register1', methods=['GET', 'POST'])
def register1():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('student-username')
        school = data.get('school')
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            conn.close()

            flash('Registration successful! Please log in.')
            return redirect('/login')
        except mysql.connector.IntegrityError:
            flash('Username already exists.')
        except Error as e:
            flash(f'Database error: {e}')
    return render_template('register.html')

@app.route('/getUserProfile', methods=['GET'])
def get_user_profile():
    user_email = session.get('user')
    if not user_email:
        return jsonify({'error': 'User is not logged in'}), 401

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM students_profile WHERE email = %s', (user_email,))
        profile = cursor.fetchone()
        conn.close()

        if profile:
            return jsonify(profile), 200
        else:
            return jsonify({'error': 'Profile not found'}), 404
    except Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500

# Route to add or update user profile
@app.route('/updateProfile', methods=['POST'])
def update_profile():    
    data = request.get_json()
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        skills = data.get('skills')
        grade_level = data.get('grade')
        school_name = data.get('school')
        bio = data.get('bio')
        interests = data.get('interests')
        gpa = data.get('gpa')
        extracurricular = data.get('extracurricular')
        cursor.execute('''
            INSERT INTO students_profile (name, email, phone, skills, grade_level, school_name, bio, interests, gpa, extracurricular)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                email = VALUES(email),
                phone = VALUES(phone),
                skills = VALUES(skills),
                grade_level = VALUES(grade_level),
                school_name = VALUES(school_name),
                bio = VALUES(bio),
                interests = VALUES(interests),
                gpa = VALUES(gpa),
                extracurricular = VALUES(extracurricular)
        ''', (name, email, phone, skills, grade_level, school_name, bio, interests, gpa, extracurricular))
        conn.commit()
        conn.close()
        flash('Profile updated successfully!')
        return redirect('/')
    except mysql.connector.IntegrityError:
        flash('Profile already exists.')
        return jsonify({'error': 'Profile already exists.'}), 400
    except Error as e:
        print(f'Database error: {e}')
        return jsonify({'error': f'Database error: {e}'}), 500

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.')
    return redirect('/login')

# Add jobs route
@app.route('/addJobs', methods=['POST'])
def add_jobs():
    try:
        # Parse job details from the request body
        data = request.get_json()
        jobTitle = data.get('jobTitle')
        jobDescription = data.get('jobDescription')
        companyName = data.get('companyName')
        jobLocation = data.get('jobLocation')
        baseSalary = data.get('baseSalary')

        # Validate input
        if not jobTitle or not jobDescription or not jobLocation or not companyName:
            return jsonify({'error': 'All fields are required'}), 400

        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert the job into the database
        cursor.execute('''
            INSERT INTO jobs (job_title, job_description, company_name, salary, job_location)
            VALUES (%s, %s, %s, %s, %s)
        ''', (jobTitle, jobDescription, companyName, baseSalary, jobLocation))

        conn.commit()
        conn.close()
        return jsonify({'message': 'Job added successfully!'}), 201
    except Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {e}'}), 500


@app.route('/getJobs', methods=['GET'])
def get_jobs():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT job_title AS jobTitle, job_description AS jobDescription, company_name AS companyName, salary AS baseSalary, job_location AS jobLocation FROM jobs")
        jobs = cursor.fetchall()
        conn.close()
        return jsonify(jobs)
    except Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500

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

@app.route('/send-email', methods=['POST'])
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

@app.route('/send-apply-job-email', methods=['POST'])
def send_apply_job_email():
    data = request.get_json()
    email = data.get('email')
    companyName = data.get('companyName')
    userEmail = session.get('user')
    if not userEmail:
        return jsonify({'error': 'User is not logged In, Email is required'}), 400
    try:
        msg = MIMEText('You have successfully applied for the job! \n\nWe will get back to you soon.')
        msg['Subject'] = f'HiIsCool: You have applied to the job at {companyName}.'
        msg['From'] = os.getenv('EMAIL_ADDRESS')
        msg['To'] = userEmail

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)