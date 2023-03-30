from domains import Task, Project, User
import tkinter as tk
from tkinter import ttk
import mysql.connector

class RegisterView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        #create widgets
        #labels
        self.nameLabel = ttk.Label(self, text = 'Name')
        self.nameLabel.grid(row = 1, column =0)
        self.emailLabel = ttk.Label(self, text = 'Email')
        self.emailLabel.grid(row = 3, column = 0)
        self.usernameLabel = ttk.Label(self, text = 'Username')
        self.usernameLabel.grid(row = 5, column = 0)
        self.passwordLabel = ttk.Label(self, text = 'Password')
        self.passwordLabel.grid(row = 7, column = 0)
        self.confirmPasswordLabel = ttk.Label(self, text = 'Confirm Password')
        self.confirmPasswordLabel.grid(row = 9, column = 0)

        #textboxes
        self.usernameVar = tk.StringVar()
        self.passwordVar = tk.StringVar()
        self.confirmPasswordVar = tk.StringVar()
        self.nameVar = tk.StringVar()
        self.emailVar = tk.StringVar()
        
        self.nameEntry = ttk.Entry(self, textvariable=self.nameVar,width = 30)
        self.nameEntry.grid(row = 2, column = 0, sticky = tk.NSEW)
        self.emailEntry = ttk.Entry(self, textvariable= self.emailVar, width = 30)
        self.emailEntry.grid(row = 4, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.usernameEntry = ttk.Entry(self, textvariable=self.usernameVar, width = 30)
        self.usernameEntry.grid(row = 6, column = 0, sticky = tk.NSEW)
        self.passwordEntry = ttk.Entry(self, textvariable=self.passwordVar, width = 30, show="*")
        self.passwordEntry.grid(row = 8, column = 0 , sticky = tk.NSEW)
        self.confirmpasswordEntry = ttk.Entry(self, textvariable=self.confirmPasswordVar, width = 30, show="*")
        self.confirmpasswordEntry.grid(row = 10, column = 0 , sticky = tk.NSEW)
        
        #register button
        self.registerButton = ttk.Button(self, text = "Register", command=self.clickRegister)
        self.registerButton.grid(row = 11, column = 0, padx = 10)

        #message 
        self.messageLabel = ttk.Label(self, text='', foreground='red')
        self.messageLabel.grid(row=12, column=0, sticky=tk.W)

        #set the controller 
        self.controller = None

    def setController(self,controller):
        self.controller = controller

    def showError(self, message):
        self.messageLabel['text'] = message
        self.messageLabel['foreground'] = 'red'
        self.messageLabel.after(3000, self.hideMessage)
 
    def hideMessage(self):
        """
        Hide the message
        :return:
        """
        self.messageLabel['text'] = ''


    def clickRegister(self):
        if self.controller:
            self.controller.registerInfo(self.nameVar.get(), self.emailVar.get(), self.usernameVar.get(), self.passwordVar.get(), self.confirmPasswordVar.get())


class RegisterController:
    def __init__(self, view):
        self.view = view
    
    def registerInfo(self, name, email, username, password, confirmPassword):
        if password == confirmPassword:
            try:
                test = User(username, password, email, name)
                test.save()
            except ValueError as error:
                self.view.showError(error)

class RegisterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title = "Login"

        #create a view and place it on the root window
        view = RegisterView(self)
        view.grid(row = 0, column = 0, padx = 10, pady = 10)

        #create the register controller
        controller = RegisterController(view)

        view.setController(controller)
if __name__ == '__main__':
    app = RegisterApp()
    app.mainloop()