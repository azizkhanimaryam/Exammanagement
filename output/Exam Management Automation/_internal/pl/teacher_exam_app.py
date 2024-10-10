from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import pyodbc
from be.Entities import Question
from bll.ExamManager import ExamManager


class AddExamDetailsDialog(tk.Toplevel):
    def __init__(self, parent, treeview, callback):
        super().__init__(parent)
        self.parent = parent
        self.title("Add Exam Details")
        self.treeview = treeview
        self.callback = callback

        # Exam Details Section
        self.exam_title_label = ttk.Label(self, text="Exam Title:")
        self.exam_title_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.exam_title_entry = ttk.Entry(self, width=50)
        self.exam_title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.exam_date_label = ttk.Label(self, text="Exam Date:")
        self.exam_date_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.exam_date_entry = ttk.Entry(self, width=50)
        self.exam_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.exam_duration_label = ttk.Label(self, text="Exam Duration (min):")
        self.exam_duration_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.exam_duration_entry = ttk.Entry(self, width=50)
        self.exam_duration_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Button to Add Exam Details
        self.add_button = ttk.Button(self, text="Save Exam Details", command=self.add_exam_details)
        self.add_button.grid(row=3, columnspan=2, padx=5, pady=5)

    def add_exam_details(self):
        # Get exam details from the entry fields
        exam_title = self.exam_title_entry.get()
        exam_date = self.exam_date_entry.get()
        exam_duration = self.exam_duration_entry.get()

        # Store the exam details in your SQL table
        try:
            # Assuming you have a method in your BLL to insert exam details
            exam_manager = ExamManager()
            exam_manager.add_exam_details(exam_title, exam_date, exam_duration)
            messagebox.showinfo("Success", "Exam details are saved successfully.")

            # Invoke the callback function to refresh the treeview
            self.callback()

            # Close the dialog
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error in saving exam details: {e}")

class AddQuestionDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Add Question")


        self.question_label = ttk.Label(self, text="Question:")
        self.question_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.question_entry = ttk.Entry(self, width=50)
        self.question_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.options_labels = []
        self.options_entries = []
        for i in range(4):
            label = ttk.Label(self, text=f"option {i + 1}:")
            label.grid(row=i + 1, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(self, width=50)
            entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky="w")
            self.options_labels.append(label)
            self.options_entries.append(entry)

        self.correct_label = ttk.Label(self, text="Correct Option")
        self.correct_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.correct_combobox = ttk.Combobox(self, values=[1, 2, 3, 4])
        self.correct_combobox.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.add_button = ttk.Button(self, text=" Add Question ", command=self.add_question)
        self.add_button.grid(row=6, columnspan=2, padx=5, pady=5)

    def add_question(self):
        # Extracting information from the dialog widgets
        question_text = self.question_entry.get()
        option1 = self.options_entries[0].get()
        option2 = self.options_entries[1].get()
        option3 = self.options_entries[2].get()
        option4 = self.options_entries[3].get()
        correct_answer = self.correct_combobox.get()  # Directly get the selected correct answer
        print("Question Text:", question_text)
        print("Options:", option1, option2, option3, option4)
        print("Correct Answer:", correct_answer)

        new_question = Question(question_text, option1, option2, option3, option4, correct_answer)
        exam = ExamManager()
        try:
            exam.add_question(new_question)
            messagebox.showinfo("Success", "Question is added sucessfully")
        except Exception as e:
            messagebox.showerror("Error", "Question adding failed")
            print(e)

        self.destroy()

class UpdateQuestionDialog(tk.Toplevel):
    def __init__(self, parent, ExamManager, question, refresh_callback):
        super().__init__(parent)
        self.parent = parent
        self.ExamManager = ExamManager
        self.question = question
        self.refresh_callback = refresh_callback
        self.title("Update Question")


        self.question_label = ttk.Label(self, text="Question:")
        self.question_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.question_entry = ttk.Entry(self, width=50)
        self.question_entry.insert("end", self.question.question_text)
        self.question_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")


        self.options_labels = []
        self.options_entries = []
        for i in range(4):
            label = ttk.Label(self, text=f"Option {i + 1}:")
            label.grid(row=i + 1, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(self, width=50)
            option_attr = getattr(self.question, f"option{i + 1}", "")  # Access option attributes directly
            entry.insert(0, option_attr)
            entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky="w")
            self.options_labels.append(label)
            self.options_entries.append(entry)

        self.correct_label = ttk.Label(self, text="Correct Option")
        self.correct_label.grid(row=len(self.question.option1) + 4, column=0, padx=5, pady=5, sticky="e")

        self.correct_combobox = ttk.Combobox(self, values=[1, 2, 3, 4])
        self.correct_combobox.insert(0,self.question.correct_answer + 1 if self.question.correct_answer is not None else "")
        self.correct_combobox.grid(row=len(self.question.option1) + 4, column=1, padx=5, pady=5, sticky="w")

        self.update_button = ttk.Button(self, text="Update", command=self.update_question)
        self.update_button.grid(row=len(self.question.option1) + 5, columnspan=2, padx=5, pady=5)

    def update_question(self):
        question_text = self.question_entry.get()
        options = [entry.get() for entry in self.options_entries]
        correct_answer_index = int(self.correct_combobox.get()) - 1
        correct_answer = options[correct_answer_index]
        print("Updating question with the following data:")
        print("Question Text:", question_text)
        print("Options:", options)
        print("Correct Answer:", correct_answer)
        self.ExamManager.update_question(
            self.question.question_id,
            question_text,
            options[0],  # option1
            options[1],  # option2
            options[2] if len(options) > 2 else "",  # option3
            options[3] if len(options) > 3 else "",  # option4
            correct_answer
        )

        self.refresh_callback()
        self.destroy()

class DeleteQuestionDialog(tk.Toplevel):
    def __init__(self, parent, questions):
        super().__init__(parent)
        self.parent = parent
        self.title("Delete Question")

        self.question_label = ttk.Label(self, text="Question list:")
        self.question_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.question_var = tk.StringVar(self)
        self.question_dropdown = ttk.Combobox(self, textvariable=self.question_var, values=question, width=47)
        self.question_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.delete_button = ttk.Button(self, text="Delete", command=self.delete_question)
        self.delete_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")
    def delete_question(self):
        selected_question = self.question_var.get()
        if selected_question:
            self.parent.delete_question(selected_question)
            self.destroy()
        else:
            messagebox.showinfo("Delete Question", "No question is selected")








class TeacherExamApp(ttk.Frame):
    def __init__(self, screen, teacher_id):
        super().__init__(screen)
        self.master = screen
        self.ExamManager = ExamManager()
        self.teacher_id = teacher_id
        self.selected_question_id = None



        add_question_button = tk.Button(self.master, text="Add Question", command=self.open_add_question_dialog)
        add_question_button.pack()

        update_question_button = tk.Button(self.master, text="Update Question", command=self.update_selected_question)
        update_question_button.pack()

        delete_selected_button = tk.Button(self.master, text="Delete Selected Question", command=self.delete_selected_question)
        delete_selected_button.pack()

        get_attempts_button = tk.Button(self.master, text="Display Attempts", command=self.display_student_attempts_table)
        get_attempts_button.pack()



        # Frame for exam details
        self.exam_details_frame = ttk.Frame(self.master)
        self.exam_details_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Add exam details button
        add_exam_details_button = tk.Button(self.exam_details_frame, text="Add Exam Details",
                                            command=self.open_add_exam_details_dialog)
        add_exam_details_button.pack(side="left", padx=5)

        # Label for exam details
        self.exam_details_label = ttk.Label(self.exam_details_frame, text="")
        self.exam_details_label.pack(side="left", padx=5)

        scrollbar = ttk.Scrollbar(self.master, orient="vertical")

        # Configure the scrollbar to scroll the Treeview
        self.tree = ttk.Treeview(self.master, columns=("question_id", "question_text", "option1","option2","option3","option4",
                                                       "correct_answer"),  show="headings")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.heading("question_id", text="Question_id")
        self.tree.heading("question_text", text="Question-text")
        self.tree.heading("option1", text="Option1")
        self.tree.heading("option2", text="Option2")
        self.tree.heading("option3", text="Option3")
        self.tree.heading("option4", text="Option4")
        self.tree.heading("correct_answer", text="Correct Option")
        self.tree.pack(fill="both", expand=True)

        scrollbar.pack(side="left", fill="y")

        self.populate_treeview()

        self.tree.bind("<ButtonRelease-1>", self.on_click_select)

    def open_add_exam_details_dialog(self):
        dialog = AddExamDetailsDialog(self.master, self.tree, self.populate_treeview)
        dialog.transient(self.master)
        dialog.grab_set()
        self.master.wait_window(dialog)

    def open_add_question_dialog(self):
        dialog = AddQuestionDialog(self)
        dialog.grab_set()

    def open_update_question_dialog(self):
        all_questions = self.ExamManager.get_all_questions()
        if all_questions:
            selected_question_id = self.selected_question_id
            print("Selected Question ID:", selected_question_id)
            selected_question = None
            for question in all_questions:
                print("Question ID:", question.question_id)
                if question.question_id == selected_question_id:
                    selected_question = question
                    break
            if selected_question:
                print("Selected Question:", selected_question)
                dialog = UpdateQuestionDialog(self.master, self.ExamManager, selected_question, self.refresh_treeview)
                dialog.grab_set()
            else:
                messagebox.showinfo("Update Question", "No Update Question with this id")
        else:
            messagebox.showinfo("Update Question", "There is no  Question")

    def update_selected_question(self):
        if self.selected_question_id is not None:
            selected_question = self.get_selected_question(self.selected_question_id)
            if selected_question:
                dialog = UpdateQuestionDialog(self.master, self.ExamManager, selected_question, self.refresh_treeview)
                dialog.grab_set()
            else:
                messagebox.showinfo("Update Question", "No Question Selected")
        else:
            messagebox.showinfo("Update Question", "No Question Selected")
    def update_question(self, question_id):
        try:
            self.ExamManager.update_question(question_id)
            messagebox.showinfo("Update Question", "Question Updated Successfully")
        except Exception as e:
            messagebox.showerror("Update Question", f"Failure in Update Question {e}")
            print(e)


    def open_delete_question_dialog(self):
        all_questions = self.ExamManager.get_all_question_texts()
        if all_questions:
            dialog = DeleteQuestionDialog(self.master, all_questions)
            dialog.grab_set()
        else:
            messagebox.showinfo("Delete Question", "There is no Question")


    def delete_selected_question(self):
        if self.selected_question_id is not None:
            print("Deleting question with ID:", self.selected_question_id)
            self.delete_question(self.selected_question_id)
            self.refresh_treeview()
        else:
            messagebox.showinfo("Delete Question", "No Question is Selected")

    def delete_question(self, question_id):
        try:
            self.ExamManager.delete_question(question_id)
            messagebox.showinfo("Delete Question", "Question Deleted Successfully")
        except Exception as e:
            messagebox.showerror("Delete Question", f"Failure in Delete Question {e}")
            print(e)

        self.refresh_treeview()


    def get_all_questions(self):
        try:
            questions = self.ExamManager.get_all_questions()
            return questions
        except Exception as e:
            messagebox.showerror("Error", f"Failure in Retrieving Question{e}")
            return []

    def on_click_select(self, event):
        item = self.tree.selection()[0]
        question_id = self.tree.item(item, "values")[0]
        self.selected_question_id = question_id
        self.selected_question = self.get_selected_question(question_id)

    def get_selected_question(self, question_id):
        try:
            return self.ExamManager.get_question_by_id(question_id)
        except Exception as e:
            print("Error getting selected question:", e)
            return None

    def populate_treeview(self):
        exam_details = self.get_exam_details_from_database()

        self.exam_details_label.config(text=" | ".join(exam_details))

        questions = self.get_all_questions()
        for question in questions:
            question_id = question.question_id
            question_text = question.question_text
            option1 = question.option1
            option2 = question.option2
            option3 = question.option3
            option4 = question.option4
            correct_answer = question.correct_answer

            self.tree.insert("", "end", values=(
                question_id, question_text, option1, option2, option3, option4, correct_answer, "", "", ""))

    def refresh_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_treeview()


    def get_exam_details_from_database(self):

        exam_details = ["Exam Title", "Exam Date", "Exam Duration(min)"]
        return exam_details

    def display_student_attempts_table(self):
        student_id = 1
        student_attempts = self.ExamManager.get_student_attempts(student_id)

        attempts_window = tk.Toplevel(self.master)
        attempts_window.title("Student Attempts")

        attempts_table = ttk.Treeview(attempts_window,
                                      columns=("exam_id", "student_id", "question_id", "chosen_answer"))
        attempts_table.heading("exam_id", text="Exam ID")
        attempts_table.heading("student_id", text="Student ID")
        attempts_table.heading("question_id", text="Question ID")
        attempts_table.heading("chosen_answer", text="Chosen Answer")
        attempts_table.pack()

        if student_attempts:
            for attempt in student_attempts:
                exam_id = attempt.get("exam_id", "N/A")
                student_id = attempt.get("student_id", "N/A")
                question_id = attempt.get("question_id", "N/A")
                chosen_answer = attempt.get("chosen_answer", "N/A")
                attempts_table.insert("", "end", values=(exam_id, student_id, question_id, chosen_answer))
        else:
            messagebox.showinfo("Student Attempts", "No attempts found for the student.")

    def get_student_attempts(self):
            student_id = 1
            student_attempts = self.ExamManager.get_student_attempts(student_id)

            if student_attempts:
                attempt_info = ""
                for attempt in student_attempts:
                    attempt_info += f"Question ID: {attempt['question_id']}, Chosen Answer: {attempt['chosen_answer']}\n"
                messagebox.showinfo("Student Attempts", attempt_info)
            else:
                messagebox.showinfo("Student Attempts", "No attempts found for the student.")
