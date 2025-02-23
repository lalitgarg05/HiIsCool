from flask import Blueprint, Flask, render_template, request, redirect, session, flash, jsonify
import mysql.connector
from config import db_config  # Ensure this is correctly configured
from mysql.connector import Error

jobs_bp = Blueprint('jobs', __name__)
@jobs_bp.route('/getJobs', methods=['GET'])
def get_jobs():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT job_title AS jobTitle, job_description AS jobDescription, company_name AS companyName, salary AS baseSalary, job_location AS jobLocation FROM jobs")
        jobs = cursor.fetchall()
        conn.close()
        return jsonify(jobs)
    except Error as e:
        return jsonify({'error': 'Database error:'}), 500

# Hiring page
@jobs_bp.route('/jobs')
def hiring():
    return render_template('jobs.html')

# Jobs page
@jobs_bp.route('/addNewJob')
def jobs():
    return render_template('postJobs.html')


# Add jobs route
@jobs_bp.route('/addJobs', methods=['POST'])
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
        return jsonify({'error': 'Database error:'}), 500
    except Exception as e:
        return jsonify({'error': 'Unexpected error: '}), 500

