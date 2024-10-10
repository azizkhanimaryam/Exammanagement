from tkinter import *
from pl.teacher_exam_app import TeacherExamApp




if __name__ == "__main__":
    teacher_Screen = Tk()
    teacher_Screen.title("Teacher Exam App")
    teacher_Screen.iconbitmap("icon.ico")
    teacher_Screen.resizable(False, False)
    PageMe = TeacherExamApp(teacher_Screen)
    teacher_Screen.mainloop()







