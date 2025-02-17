from flask import Flask, render_template, request, redirect, session, flash, jsonify
import mysql.connector
from mysql.connector import Error
from config import db_config
import logging


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
    
# Add jobs route
@app.route('/addJobs', methods=['POST'])
def add_jobs():
    app.logger.debug(f"Request Content-Type: {request.content_type}")
    app.logger.debug(f"Request Data: {request.data}")
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


if __name__ == '__main__':
    app.run(debug=True)  # Use a different port if needed
