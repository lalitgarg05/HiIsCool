import mysql.connector
from mysql.connector import Error

# Function to create a database if it doesn't exist
def create_database():
    try:
        # Hardcoded database connection details
        host = 'localhost'
        user = 'root'
        password = 'Kanha@123'  # Replace with your actual password
        
        # Connect to MySQL
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        if conn.is_connected():
            cursor = conn.cursor()
            # Create the database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS job_database")
            conn.close()
            print("Database created successfully.")
        else:
            print("Failed to connect to MySQL.")
    except Error as e:
        print(f"Error: {e}")

# Function to create the jobs table
def create_table():
    try:
        # Hardcoded connection details with the database
        host = 'localhost'
        user = 'root'
        password = 'Kanha@123'  # Replace with your actual password
        database = 'hiiscool'  # Name of the database to use

        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            title VARCHAR(255) NOT NULL,
                            company VARCHAR(255) NOT NULL,
                            location VARCHAR(255) NOT NULL,
                            description TEXT)''')
        conn.commit()
        conn.close()
        print("Table created successfully.")
    except Error as e:
        print(f"Error: {e}")

# Function to add a new job to the database
def add_job(title, company, location, description):
    try:
        # Hardcoded connection details
        host = 'localhost'
        user = 'root'
        password = 'Kanha@123'  # Replace with your actual password
        database = 'hiiscool'  # Name of the database to use

        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO jobs (job_title, company_name, job_location, job_description)
                          VALUES (%s, %s, %s, %s)''', (title, company, location, description))
        conn.commit()
        print("Job added successfully!")
        conn.close()
    except Error as e:
        print(f"Error: {e}")

# Function to display all jobs in the database
def view_jobs():
    try:
        # Hardcoded connection details
        host = 'localhost'
        user = 'root'
        password = 'Kanha@123'  # Replace with your actual password
        database = 'hiiscool'  # Name of the database to use

        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()

        for job in jobs:
            print(f"ID: {job[0]}, Title: {job[1]}, Company: {job[2]}, Location: {job[3]}, Description: {job[4]}")
        
        conn.close()
    except Error as e:
        print(f"Error: {e}")

# Main function to interact with the user
def main():
    create_database()  # Ensure the database is created
    create_table()     # Ensure the table is created

    print("Welcome to the job listing system!")
    while True:
        action = input("Would you like to (a)dd a new job or (v)iew all jobs? (Enter 'q' to quit): ").lower()

        if action == 'a':
            title = input("Enter the job title: ")
            company = input("Enter the company name: ")
            location = input("Enter the job location: ")
            description = input("Enter the job description: ")
            add_job(title, company, location, description)
        elif action == 'v':
            view_jobs()
        elif action == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
