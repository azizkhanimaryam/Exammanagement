import pyodbc
from be.Setting import Setting
from be.Entities import Question, Exam

conn = Setting().GetConnectionString()

class DataAccess:
    def __init__(self):
        self.conn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=.;DATABASE=ExamManagement;Trusted_Connection=yes;")
        self.cursor = self.conn.cursor()

    def add_exam_details(self, exam_title, exam_date, exam_duration):
        try:
            query = "INSERT INTO Exam (exam_title, exam_date, exam_duration) VALUES (?, ?, ?)"
            values = (exam_title, exam_date, exam_duration)
            self.cursor.execute(query, values)
            self.conn.commit()
            print("مشخصات آزمون با موفقیت اضافه شد")
            return True

        except Exception as e:
            print("مشخصات آزمون اضافه نشد")
            print(e)

    def get_latest_exam_details(self):
        try:
            query = """
            SELECT TOP 1 exam_title, exam_date, exam_duration
            FROM Exam
            ORDER BY exam_date DESC
            """
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row:
                exam_title, exam_date, exam_duration = row
                return Exam(exam_title, exam_date, exam_duration)
            else:
                print("No exam details found.")
                return None
        except Exception as e:
            print("Error fetching exam details:", e)
            return None

    def validate_student(self, student_id):
        try:
            # Check if the student ID exists in the Student table
            query = "SELECT COUNT(*) FROM Student WHERE student_id = ?"
            self.cursor.execute(query, (student_id,))
            count = self.cursor.fetchone()[0]
            if count > 0:
                return True  # Student ID exists
            else:
                return False  # Student ID does not exist
        except pyodbc.Error as e:
            print("Error validating student:", e)
            return False

    def validate_teacher(self, teacher_id):
        try:
            # Check if the teacher ID exists in the Teacher table
            query = "SELECT COUNT(*) FROM Teacher WHERE teacher_id = ?"
            self.cursor.execute(query, (teacher_id,))
            count = self.cursor.fetchone()[0]
            return count > 0  # Return True if teacher ID exists, False otherwise
        except pyodbc.Error as e:
            # Log or handle the error
            print("Error validating teacher:", e)
            return False



    def add_question(self, question_text, option1, option2, option3, option4, correct_answer):
        try:
            query = "INSERT INTO Question (question_text, option1, option2, option3, option4, correct_answer) VALUES (?, ?, ?, ?, ?, ?)"
            params = (question_text, option1, option2, option3, option4, correct_answer)
            self.cursor.execute(query, params)
            self.conn.commit()
            print("سوال با موفقیت اضافه شد")
            return True
        except Exception as e:
            print("سوال اضافه نشد")
            print(e)
            return False

    def update_question(self, question_id, question_text, option1, option2, option3, option4, correct_answer):
        try:
            query = ("UPDATE Question SET question_text = ?, option1 = ?, option2 = ?, option3 = ?, option4 = ?, "
                     "correct_answer = ? WHERE question_id = ?")
            params = (question_text, option1, option2, option3, option4, correct_answer, question_id)
            print("Executing update query...")
            print("Query:", query)
            print("Params:", params)
            self.cursor.execute(query, params)
            self.cursor.commit()
            print("سوال با موفقیت به روزرسانی شد")
            return True
        except Exception as e:
            print("سوال به روزرسانی نشد")
            print(e)
            return False

    def get_selected_question(self, question_id):
        try:
            query = "SELECT * FROM Question WHERE question_id = ?"
            self.cursor.execute(query, (question_id,))
            row = self.cursor.fetchone()
            if row:
                question_text = row[1]
                options = row[2:6]
                correct_answer = row[6]
                return Question(question_text, options, correct_answer)
            else:
                return None
        except Exception as e:
            print("Error:", e)
            return None

    def get_all_questions(self):
        try:
            query = "SELECT * FROM Question"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print("Error getting all questions:", e)
            return []

    def delete_question(self, question_id):
        try:
            query = "DELETE FROM Question WHERE question_id = ?"
            self.cursor.execute(query, (question_id,))
            self.conn.commit()
            print("سوال با موفقیت حذف شد.")
        except Exception as e:
            print("خطا در حذف سوال:", e)

    def get_all_question_ids(self):
        try:
            query = "SELECT question_id FROM Question"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            print("Error getting all question IDs:", e)
            return []

    def get_question_by_id(self, question_id):
        try:
            query = "SELECT question_text, option1, option2, option3, option4, correct_answer FROM Question WHERE question_id = ?"
            self.cursor.execute(query, (question_id,))
            row = self.cursor.fetchone()
            if row:
                question_text, option1, option2, option3, option4, correct_answer = row
                return Question(question_text, option1, option2, option3, option4, correct_answer)
            else:
                return None
        except Exception as e:
            print(f"Error fetching question with ID {question_id}: {e}")
            return None

    def save_attempt(self, attempt):
        try:
            # Ensure that student_id is an integer
            if not isinstance(attempt.student_id, int):
                raise ValueError("Student ID must be an integer")

            query = "INSERT INTO ExamAttempt (question_id, chosen_answer, student_id) VALUES (?, ?, ?)"
            params = (attempt.question_id, attempt.chosen_answer, attempt.student_id)
            self.cursor.execute(query, params)
            self.conn.commit()
            print("Attempt saved successfully")
            return True
        except Exception as e:
            print("Failed to save attempt:", e)
            return False

    def get_student_attempts(self, student_id):
        try:
            query = """
            SELECT ExamAttempt.attempt_id, ExamAttempt.question_id, Question.question_text, ExamAttempt.chosen_answer
            FROM ExamAttempt
            JOIN Question ON ExamAttempt.question_id = Question.question_id
            WHERE ExamAttempt.student_id = ?
            """
            self.cursor.execute(query, (student_id,))
            rows = self.cursor.fetchall()
            attempts = []
            for row in rows:
                attempt_id, question_id, question_text, chosen_answer = row
                attempts.append({"attempt_id": attempt_id, "question_id": question_id, "question_text": question_text,
                                 "chosen_answer": chosen_answer})
            return attempts
        except Exception as e:
            print("Error fetching student attempts:", e)
            return []

    def display_student_answers(self, student_id):
        student_attempts = self.get_student_attempts(student_id)
        if student_attempts:
            for attempt in student_attempts:
                question_id = attempt.question_id
                chosen_answer = attempt.chosen_answer
                print(f"Question ID: {question_id}, Chosen Answer: {chosen_answer}")
        else:
            print("No answers found for the student.")