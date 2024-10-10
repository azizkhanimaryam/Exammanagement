import pyodbc

try:
    # Establish connection
    connection = pyodbc.connect(
        driver='{ODBC Driver 17 for SQL Server}',
        server='.',
        database='ExamManagement',
        trusted_connection='yes'
    )
    print("Connection to SQL Server database successful")

    # Do something with the connection
except pyodbc.Error as e:
    # Handle connection errors
    print(f"Error connecting to SQL Server database: {e}")




    def validate_teacher_id(self, teacher_id):
        try:
            # Call the validate_teacher method from DataAccess
            return self.repos.validate_teacher(teacher_id)
        except Exception as e:
            print("Error validating teacher ID:", e)
            return False

    def validate_student_id(self, student_id):
        try:
            # Call the validate_student method from DataAccess
            return self.repos.validate_student(student_id)
        except Exception as e:
            print("Error validating student ID:", e)
            return False

