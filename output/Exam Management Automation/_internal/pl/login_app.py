import tkinter as tk
from tkinter import ttk, messagebox
from bll.ExamManager import ExamManager
from pl.teacher_exam_app import TeacherExamApp
from pl.student_exam_app import StudentExamApp
from be.Entities import Exam


class LoginApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Login")
        self.pack(fill=tk.BOTH, expand=True)

        login_frame = ttk.Frame(self)
        login_frame.pack(padx=20, pady=20)

        # Label and Entry for entering ID
        id_label = ttk.Label(login_frame, text="Enter your ID:")
        id_label.grid(row=0, column=0, sticky="w")

        self.id_entry = ttk.Entry(login_frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Combobox for selecting role
        role_label = ttk.Label(login_frame, text="Select your role:")
        role_label.grid(row=1, column=0, sticky="w")

        self.role_combo = ttk.Combobox(login_frame, values=["Teacher", "Student"])
        self.role_combo.grid(row=1, column=1, padx=5, pady=5)

        # Button for login
        login_button = ttk.Button(login_frame, text="Login", command=self.login)
        login_button.grid(row=2, columnspan=2, pady=10)

    def validate_id(self, user_id, role):
        try:
            # Assuming you have a method in ExamManager to validate teacher and student IDs
            is_teacher, is_student = ExamManager().validate_id(user_id, role)
            return is_teacher, is_student
        except Exception as e:
            print("Error validating ID:", e)
            return False, False

    def login(self):
        user_id = self.id_entry.get()
        role = self.role_combo.get()

        if not user_id:
            messagebox.showerror("Error", "Please enter your ID.")
            return

        if not role:
            messagebox.showerror("Error", "Please select your role.")
            return

        # Validate the entered ID
        is_teacher, is_student = self.validate_id(user_id, role)

        if role == "Teacher" and is_teacher:
            # Redirect to teacher interface
            self.redirect_to_teacher_interface(user_id)
        elif role == "Student" and is_student:
            # Redirect to student interface
            self.redirect_to_student_interface(user_id)
        else:
            messagebox.showerror("Error", "Invalid ID or role. Please try again.")

    def redirect_to_teacher_interface(self, teacher_id):
        # Create and display the teacher interface
        teacher_Screen = tk.Tk()
        teacher_Screen.title("Teacher Exam App")
        #teacher_Screen.iconbitmap("icon.ico")
        teacher_Screen.resizable(False, False)
        teacher_app = TeacherExamApp(teacher_Screen, teacher_id)
        self.master.withdraw()

    def redirect_to_student_interface(self, student_id, teacher_id=None):
        # Create and display the student interface after successful login
        student_Screen = tk.Tk()
        student_Screen.geometry("%dx%d+%d+%d" % (800, 600, 720, 400))
        student_Screen.title("Student Exam App")
        #student_Screen.iconbitmap("icon.ico")
        student_Screen.resizable(True, True)
        PageMe = StudentExamApp(student_Screen, ExamManager(), student_id)
        PageMe.teacher_id = teacher_id  # Set the teacher_id here
        #PageMe.submit_attempt()
        PageMe.pack(fill=tk.BOTH, expand=True)
        print("Widgets in StudentExamApp:", PageMe.winfo_children())  # Debug: Print widgets in StudentExamApp
        self.master.withdraw()


# Usage
def main():
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
