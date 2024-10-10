from be.Entities import Exam
from dal.Repository import DataAccess

repos = DataAccess()


class ExamManager:
    def __init__(self):
        self.repos = DataAccess()
        self.question_ids = []
        self.current_question_index = 0
        self.question_ids = self.repos.get_all_question_ids()

    def validate_id(self, user_id, role):
        try:
            if role == "Teacher":
                return self.repos.validate_teacher(user_id), False
            elif role == "Student":
                return False, self.repos.validate_student(user_id)
            else:
                print("Invalid role:", role)
                return False, False
        except Exception as e:
            print("Error validating ID:", e)
            return False, False



    def add_exam_details(self, exam_title, exam_date, exam_duration):
        try:
            self.repos.add_exam_details(exam_title, exam_date, exam_duration)
        except Exception as e:
            print("Error adding exam details:", e)
            raise e

    def get_exam_details(self):
        try:
            # Assuming you have a method to retrieve the latest exam details from the repository
            exam_details = self.repos.get_latest_exam_details()
            if exam_details:
                # Assuming exam_details is a namedtuple or a similar data structure
                return Exam(exam_details.exam_title, exam_details.exam_date, exam_details.exam_duration)
            else:
                print("No exam details found.")
                return None
        except Exception as e:
            print("Error fetching exam details:", e)
            return None

    def add_question(self, question):
        return repos.add_question(question.question_text,
                                  question.option1,
                                  question.option2,
                                  question.option3,
                                  question.option4,
                                  question.correct_answer)


    def update_question(self, question_id, question_text, option1, option2, options3,
                                                 options4, correct_answer):
        try:
            print("Attempting to update question...")
            success = self.repos.update_question(question_id, question_text, option1, option2, options3,
                                                 options4, correct_answer)
            if success:
                print("Question updated successfully.")
            else:
                print("Question update failed.")
            return success
        except Exception as e:
            print("سوال به روزرسانی نشد")
            print(e)
            return False

    def get_question_by_id(self, question_id):
        try:
            question = self.repos.get_question_by_id(question_id)
            if question and hasattr(question, 'question_text') and hasattr(question, 'option1') and hasattr(question,
                                                                                                            'option2') and hasattr(
                    question, 'option3') and hasattr(question, 'option4') and hasattr(question, 'correct_answer'):
                return question
            else:
                print(f"Error: Question with ID {question_id} is missing necessary fields.")
                return None
        except Exception as e:
            print(f"Error fetching question with ID {question_id}: {e}")
            return None

    def get_all_questions(self):
        return repos.get_all_questions()

    def delete_question(self, question_id):
        try:
            self.repos.delete_question(question_id)
            print("سوال با موفقیت حذف شد.")
        except Exception as e:
            print("خطا در حذف سوال:", e)

    def get_all_question_ids(self):
        try:
            return self.repos.get_all_question_ids()
        except Exception as e:
            print("Error getting all question IDs:", e)
            return []

    def get_next_question(self):
        print("Current question index:", self.current_question_index)
        if self.current_question_index < len(self.question_ids):
            self.question_id = self.question_ids[self.current_question_index]
            print("Loading question with ID:", self.question_id)
            question = self.repos.get_question_by_id(self.question_id)
            self.current_question_index += 1
            return question
        else:
            print("No more questions available.")
            return None

    def reset_question_index(self):
        self.current_question_index = 0

    def save_attempt(self, attempt):
        try:
            self.repos.save_attempt(attempt)
        except Exception as e:
            print("Failed to save attempt:", e)

    def get_student_attempts(self, student_id):
        try:
            return self.repos.get_student_attempts(student_id)
        except Exception as e:
            print("Error getting student attempts:", e)
            return None

    def display_student_answers(self, student_id):
        student_attempts = self.repos.get_student_attempts(student_id)
        for attempt in student_attempts:
            print(f"Attempt ID: {attempt['attempt_id']}")
            print(f"Question: {attempt['question_text']}")
            print(f"Chosen Answer: {attempt['chosen_answer']}\n")
