import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from be.Entities import ExamAttempt, Student, Teacher, Question
from bll.ExamManager import ExamManager


class StudentExamApp(ttk.Frame):
    def __init__(self, master, ExamManager, student_id, teacher_id=None):
        super().__init__(master)
        self.master = master
        self.master.title("Student Exam App")
        self.pack(fill=tk.BOTH, expand=True)
        self.ExamManager = ExamManager
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.current_question_id = None
        self.selected_option = tk.StringVar()
        self.exam_details = None
        self.create_widgets()
        self.load_exam_details()

    def create_widgets(self):

        # Display exam details
        self.exam_details_label = ttk.Label(self, text="Exam Details:")
        self.exam_details_label.pack()

        self.exam_details_text = tk.Text(self, wrap=tk.WORD, height=5, width=50)
        self.exam_details_text.pack()
        self.question_label = ttk.Label(self, text="Question:")
        self.question_label.pack()

        self.question_text = tk.Text(self, wrap=tk.WORD, height=5, width=50)
        self.question_text.pack()

        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.pack(fill=tk.BOTH, expand=True)

        self.option_radiobuttons = []
        self.options = []

        for i in range(4):
            radiobutton = ttk.Radiobutton(self.options_frame, text=f"Option {i + 1}", variable=self.selected_option,
                                          value=str(i + 1), command=self.on_option_selected)
            radiobutton.pack(anchor=tk.W)
            self.option_radiobuttons.append(radiobutton)


        self.load_question_button = ttk.Button(self, text="Load Question", command=self.load_question)
        self.load_question_button.pack()

        self.submit_button = ttk.Button(self, text="Submit Attempt", command=self.submit_attempt)
        self.submit_button.pack()

    def load_exam_details(self):
        # Fetch exam details using ExamManager
        self.exam_details = self.ExamManager.get_exam_details()
        if self.exam_details:
            # Display exam details in the text widget
            self.exam_details_text.delete('1.0', tk.END)
            self.exam_details_text.insert(tk.END, f"Title: {self.exam_details.exam_title}\n"
                                                  f"Date: {self.exam_details.exam_date}\n"
                                                  f"Duration: {self.exam_details.exam_duration} minutes")

    def load_question(self):
        question = self.ExamManager.get_next_question()
        if question:
            self.current_question_id = question.question_id
            self.question_text.delete('1.0', tk.END)
            self.question_text.insert(tk.END, question.question_text)
            options = [question.option1, question.option2, question.option3, question.option4]
            self.selected_option.set("")  # Reset selected option
            for i, radiobutton in enumerate(self.option_radiobuttons):
                radiobutton.config(text=options[i])
                radiobutton.update()
        else:
            messagebox.showinfo("Info", "You Have Answered All Questions!")

    def submit_attempt(self):
        selected_option = self.selected_option.get()
        print("Before submitting attempt - Selected option:", selected_option)

        if not selected_option:
            messagebox.showerror("Error", "Please Select an Option")
            return

        attempt = ExamAttempt(
            student_id=self.student_id,
            teacher_id=self.teacher_id,
            question_id=self.current_question_id,
            chosen_answer=int(selected_option)
        )

        try:
            self.ExamManager.save_attempt(attempt)
            messagebox.showinfo("Success", "Attempts Submitted Successfully!")
            self.load_question()
        except Exception as e:
            messagebox.showerror("Error", f"Failure in Submitting Attempts! {e}")

    def close_window(self):
        self.master.destroy()

    def on_option_selected(self):
        selected_option = self.selected_option.get()
        print("Selected option:", selected_option)


student_id = "your_student_id_here"


