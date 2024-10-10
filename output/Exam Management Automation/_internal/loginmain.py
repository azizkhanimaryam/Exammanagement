from tkinter import *
from pl.login_app import LoginApp
from be.db import dbContext


if __name__ == "__main__":
    db=dbContext()
    login_Screen = Tk()
    login_Screen.title("Login App")
    login_Screen.resizable(False, False)
    PageMe = LoginApp(login_Screen)
    login_Screen.mainloop()