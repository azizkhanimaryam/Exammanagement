from tkinter import *
import tkinter as tk
from bll.ExamManager import ExamManager
from pl.student_exam_app import StudentExamApp
from be.Entities import Exam


ExamManager = ExamManager()

student_id = "your_student_id_here"
student_name = "your_student_name_here"
teacher_id = "your_teacher_id_here"

if __name__ == "__main__":
    student_Screen = Tk()
    student_Screen.geometry("%dx%d+%d+%d" % (800, 600, 720, 400))
    student_Screen.title("Student Exam App")
    student_Screen.iconbitmap("icon.ico")
    student_Screen.resizable(True, True)
    PageMe = StudentExamApp(student_Screen, ExamManager, student_id)
    PageMe.pack(fill=tk.BOTH, expand=True)
    print("Widgets in StudentExamApp:", PageMe.winfo_children())
    student_Screen.mainloop()
