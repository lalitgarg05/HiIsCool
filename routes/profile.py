from flask import Blueprint, render_template, request, jsonify, session, redirect, flash
import mysql.connector
from mysql.connector import Error
from config import db_config

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
def profile():
    return render_template('profile.html')

@profile_bp.route('/getUserProfile', methods=['GET'])
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

@profile_bp.route('/updateProfile', methods=['POST'])
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