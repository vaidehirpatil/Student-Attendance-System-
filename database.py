import sqlite3

# Create a connection to the SQLite database
connection = sqlite3.connect("database.db")

# Create a cursor object
cursor = connection.cursor()

# Create the 'students' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        month_name TEXT, 
        student_name TEXT, 
        present_days INTEGER, 
        absent_days INTEGER
    )
""")

# Define the list of students
student_list = [
    ("January", "Raj Modi", 20, 2),
    ("January", "Arnav Khanna", 22, 0)
]

# Insert data into the table
cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?)", student_list)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database created and data inserted successfully!")