import mysql.connector  # Importing the MySQL connector library to interact with MySQL databases.
from mysql.connector import Error  # Importing the Error class to handle MySQL connection errors.

# Function to create a database if it doesn't exist
def create_database():
    try:
        # Hardcoded database connection details
        host = 'localhost'  # Host where the MySQL server is running.
        user = 'root'  # MySQL username.
        password = 'Kanha@123'  # Replace with your actual MySQL password.
        
        # Connect to MySQL
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        if conn.is_connected():  # Check if the connection to MySQL is successful.
            cursor = conn.cursor()  # Create a cursor object to execute SQL queries.
            # Create the database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS job_database")  # SQL query to create the database.
            conn.close()  # Close the database connection.
            print("Database created successfully.")  # Inform the user that the database has been created.
        else:
            print("Failed to connect to MySQL.")  # Inform the user if the connection fails.
    except Error as e:  # Handle any errors that occur during the process.
        print(f"Error: {e}")  # Print the error message.

# Function to create the jobs table
def create_table():
    try:
        # Hardcoded connection details with the database
        host = 'localhost'  # Host where the MySQL server is running.
        user = 'root'  # MySQL username.
        password = 'Kanha@123'  # Replace with your actual MySQL password.
        database = 'hiiscool'  # Name of the database to use.

        # Connect to the specific database
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()  # Create a cursor object to execute SQL queries.
        # SQL query to create a table if it doesn't already exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                            id INT AUTO_INCREMENT PRIMARY KEY,  # Unique ID for each job, auto-incremented.
                            title VARCHAR(255) NOT NULL,  # Job title, cannot be NULL.
                            company VARCHAR(255) NOT NULL,  # Company name, cannot be NULL.
                            location VARCHAR(255) NOT NULL,  # Job location, cannot be NULL.
                            description TEXT)''')  # Job description with a variable text size.
        conn.commit()  # Commit the changes to the database.
        conn.close()  # Close the database connection.
        print("Table created successfully.")  # Inform the user that the table has been created.
    except Error as e:  # Handle any errors that occur during the process.
        print(f"Error: {e}")  # Print the error message.

# Function to add a new job to the database
def add_job(title, company, location, description, salary):
    try:
        # Hardcoded connection details
        host = 'localhost'  # Host where the MySQL server is running.
        user = 'root'  # MySQL username.
        password = 'Kanha@123'  # Replace with your actual MySQL password.
        database = 'hiiscool'  # Name of the database to use.

        # Connect to the database
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()  # Create a cursor object to execute SQL queries.
        # SQL query to insert a new job into the jobs table
        cursor.execute('''INSERT INTO jobs (job_title, company_name, job_location, job_description, salary)
                          VALUES (%s, %s, %s, %s, %s)''', (title, company, location, description, salary))
        conn.commit()  # Commit the changes to the database.
        print("\nJob added successfully!")  # Inform the user that the job has been added.
        conn.close()  # Close the database connection.
    except Error as e:  # Handle any errors that occur during the process.
        print(f"Error: {e}")  # Print the error message.

# Function to display all jobs in the database
def view_jobs():
    try:
        # Hardcoded connection details
        host = 'localhost'  # Host where the MySQL server is running.
        user = 'root'  # MySQL username.
        password = 'Kanha@123'  # Replace with your actual MySQL password.
        database = 'hiiscool'  # Name of the database to use.

        # Connect to the database
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()  # Create a cursor object to execute SQL queries.
        cursor.execute("SELECT * FROM jobs")  # SQL query to fetch all records from the jobs table.
        jobs = cursor.fetchall()  # Fetch all the rows returned by the query.

        # Iterate over each job and print its details
        for job in jobs:
            print(f"ID: {job[0]}, Title: {job[1]}, Company: {job[3]}, Location: {job[5]}, Description: {job[2]}, Salary: {job[4]}")
        
        conn.close()  # Close the database connection.
    except Error as e:  # Handle any errors that occur during the process.
        print(f"Error: {e}")  # Print the error message.

# Main function to interact with the user
def main():
    create_database()  # Ensure the database is created
    create_table()     # Ensure the table is created

    print("Welcome to the job listing system!\n")  # Welcome message for the user.
    while True:
        # Prompt the user for an action
        action = input("Would you like to (a)dd a new job or (v)iew all jobs? (Enter 'q' to quit): ").lower()

        if action == 'a':  # If the user wants to add a new job
            title = input("Enter the job title: ")  # Get the job title from the user.
            company = input("Enter the company name: ")  # Get the company name from the user.
            location = input("Enter the job location: ")  # Get the job location from the user.
            description = input("Enter the job description: ")  # Get the job description from the user.
            salary = input("Enter the Salary: ")  # Get the salary from the user.
            add_job(title, company, location, description, salary)  # Add the new job to the database.
        elif action == 'v':  # If the user wants to view all jobs
            view_jobs()  # Call the function to display all jobs.
        elif action == 'q':  # If the user wants to quit
            print("\nGoodbye!")  # Farewell message.
            break  # Exit the loop and end the program.
        else:
            print("Invalid input. Please try again.")  # Handle invalid inputs.

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()