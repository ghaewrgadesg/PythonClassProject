from domains import Task, Project, User
import tkinter as tk
from tkinter import ttk
import mysql.connector
from RegisterWindowGUI import RegisterView,RegisterController,RegisterApp
from ProjectSelectorGUI import ProjectSelectorView, ProjectSelectorController, ProjectSelectorApp

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
        self.usernameEntry = ttk.Entry(self, textvariable=self.usernameVar, width = 60)
        self.usernameEntry.grid(row = 2, column = 0, columnspan = 2)
        self.passwordEntry = ttk.Entry(self, textvariable=self.passwordVar, width = 60, show="*")
        self.passwordEntry.grid(row = 4, column = 0, columnspan = 2)

        #Login button
        self.loginButton = ttk.Button(self, text = "Login", command=self.clickLogin)
        self.loginButton.grid(row = 5, column = 0, padx=10)

        #register button
        self.registerButton = ttk.Button(self, text = "Register", command=self.clickRegister)
        self.registerButton.grid(row = 5, column = 1, padx = 10)

        #message 
        self.messageLabel = ttk.Label(self, text='', foreground='red')
        self.messageLabel.grid(row=6, column=0, sticky=tk.W)

        #set the controller
        self.controller = None

    def setController(self, controller):
        self.controller = controller

    def clickLogin(self):
        if self.controller:
            self.controller.login(self.usernameVar.get(), self.passwordVar.get())
    
    def showError(self, message):
        self.messageLabel['text'] = message
        self.messageLabel['foreground'] = 'red'
        self.messageLabel.after(3000, self.hideMessage)
 
    def showMessage(self, message):
        self.messageLabel['text'] = message
        self.messageLabel['foreground'] = 'green'
        self.messageLabel.after(3000, self.hideMessage)

    def hideMessage(self):
        """
        Hide the message
        :return:
        """
        self.messageLabel['text'] = ''

    def clickRegister(self):
        if self.controller:
            self.controller.register()

class LoginController:
    def __init__(self, view, app):
        self.view = view
        self.app = app
        with open("databasePassword.txt") as f:
            databasePassword = f.readline().rstrip()
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=databasePassword
        )
    
    def login(self,username, password):
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("SELECT `username`, `password` FROM Users")
        loginInfo = mycursor.fetchall()
        for i in loginInfo:
            if username == i[0] and password == i[1]:
                mycursor.execute("SELECT `username`,`password`, `email`, `name` FROM Users WHERE `Username` = '{}'".format(i[0]))
                loginInfo = mycursor.fetchall()[0]
                loginUser = User(loginInfo[0], loginInfo[1], loginInfo[2], loginInfo[3])
                self.app.destroy()
                self.Selectorapp = ProjectSelectorApp(loginUser)
                self.Selectorapp.mainloop()
            else:
                self.view.showError("Invalid info")
    
    def register(self):
        self.registerWindow = RegisterApp()

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Login")
        #create a view and place it on the root window
        view = LoginView(self)
        view.grid(row = 0, column = 1, padx = 10, pady = 10)

        #create the login controller
        controller = LoginController(view,self)

        view.setController(controller)
if __name__ == '__main__':
    app = LoginApp()
    app.mainloop()
