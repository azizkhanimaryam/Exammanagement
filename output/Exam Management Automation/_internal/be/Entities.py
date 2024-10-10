from sqlalchemy.orm import sessionmaker, declarative_base,relationship
from sqlalchemy import create_engine, Column, Integer, String, NVARCHAR, ForeignKey
from be.Setting import Setting

import pyodbc

conn = Setting().GetConnectionString()
engine = create_engine('sqlite:///ExamManagement.db')
engine = create_engine(str(conn))
Base = declarative_base()



class Exam(Base):
    __tablename__ = "Exam"
    exam_id = Column(Integer, primary_key=True)
    exam_title = Column(NVARCHAR)
    exam_date = Column(NVARCHAR)
    exam_duration = Column(Integer)
    questions = relationship("Question", back_populates="exam")

    def __init__(self, exam_title, exam_date, exam_duration):
        self.exam_title = exam_title
        self.exam_date = exam_date
        self.exam_duration = exam_duration

    def __repr__(self):
        return f"<Exam(exam_id={self.exam_id}, exam_title='{self.exam_title}')>"



class Question(Base):
    __tablename__ = "Question"
    question_id = Column(Integer, primary_key=True)
    question_text = Column(NVARCHAR)
    option1 = Column(NVARCHAR)
    option2 = Column(NVARCHAR)
    option3 = Column(NVARCHAR)
    option4 = Column(NVARCHAR)
    correct_answer = Column(Integer)
    exam_id = Column(Integer, ForeignKey('Exam.exam_id'))
    attempts = relationship("ExamAttempt", back_populates="question")
    exam = relationship("Exam", back_populates="questions")


    def __init__(self, question_text, option1, option2, option3, option4, correct_answer, exam_id=None):
        self.question_text = question_text
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.correct_answer = correct_answer
        self.exam_id = exam_id

    def __repr__(self):
        return f"<Question(question_id={self.question_id}, question_text='{self.question_text}')>"


class Teacher(Base):
    __tablename__ = "Teacher"
    teacher_id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_name = Column(NVARCHAR)
    attempts = relationship("ExamAttempt", back_populates="teacher")

    def __init__(self, teacher_name):
        self.teacher_name = teacher_name

    def __repr__(self):
        return f"<Teacher(teacher_id={self.teacher_id}, teacher_name='{self.teacher_name}')>"

class Student(Base):
    __tablename__ = "Student"
    student_id = Column(Integer, primary_key=True)
    student_name = Column(NVARCHAR)
    attempts = relationship("ExamAttempt", back_populates="student")

    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name

    def __repr__(self):
        return f"<Student(student_id={self.student_id}, student_name='{self.student_name}')>"

class ExamAttempt(Base):
    __tablename__ = "ExamAttempt"
    attempt_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('Student.student_id'))
    teacher_id = Column(Integer, ForeignKey('Teacher.teacher_id'))
    question_id = Column(Integer, ForeignKey('Question.question_id'))
    chosen_answer = Column(Integer)
    student = relationship("Student", back_populates="attempts")
    question = relationship("Question", back_populates="attempts")
    teacher = relationship("Teacher", back_populates="attempts")



    def __init__(self, teacher_id, student_id, question_id, chosen_answer):
        self.teacher_id = teacher_id
        self.student_id = student_id
        self.question_id = question_id
        self.chosen_answer = chosen_answer

    def __repr__(self):
        return f"<ExamAttempt(attempt_id={self.attempt_id},teacher_id={self.teacher_id},  student_id={self.student_id}, question_id={self.question_id}, chosen_answer={self.chosen_answer})>"


Base.metadata.create_all(engine)
