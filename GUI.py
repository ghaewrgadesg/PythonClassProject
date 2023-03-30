from domains import Task, Project, User
import tkinter as tk
from tkinter import ttk
import mysql.connector

class LoginView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #create widgets
        #label
        self.usernameLabel = ttk.Label(self, text = 'Username')
        self.usernameLabel.grid(row = 1, column = 0, columnspan = 2)
        self.passwordLabel = ttk.Label(self, text = 'Password')
        self.passwordLabel.grid(row = 3, column = 0, columnspan = 2)

        #textbox
        self.usernameVar = tk.StringVar()
        self.passwordVar = tk.StringVar()
        self.usernameEntry = ttk.Entry(self, textvariable=self.usernameVar, width = 30)
        self.usernameEntry.grid(row = 2, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.passwordEntry = ttk.Entry(self, textvariable=self.passwordVar, width = 30)
        self.passwordEntry.grid(row = 4, column = 0, columnspan = 2, sticky = tk.NSEW)

        #Login button
        self.loginButton = ttk.Button(self, text = "Login", command=self.clickLogin)
        self.loginButton.grid(row = 5, column = 0, padx=10)

        #register button
        self.registerButton = ttk.Button(self, text = "Register", command=self.clickRegister')
        self.registerButton.grid(row = 5, column = 1, padx = 10)

        #set the controller
        self.controller = None

    def setController(self, controller):
        self.controller = controller

    def clickLogin(self):
        if self.controller:
            self.controller.login(self.usernameEntry.get(), self.passwordEntry.get())
    
    def clickRegister(self):
        print("to be finished")

class LoginController:
    def __init__(self, view):
        self.view = view

    def login(self,username, password):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ch0keYourselfT0Sle#p"
        )
        mycursor = mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("SELECT `username`, `password` FROM Users")
        loginInfo = mycursor.fetchall()
        for i in loginInfo:
            if username == i[0] and password == i[1]:
                print("Login Succedded")
class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title = "Login"

        #create a view and place it on the root window
        view = LoginView(self)
        view.grid(row = 0, column = 0, padx = 10, pady = 10)

        #create the login controller
        controller = LoginController(view)

        view.setController(controller)

if __name__ == '__main__':
    app = LoginApp()
    app.mainloop()

