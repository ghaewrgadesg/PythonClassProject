from domains import Task, Project, User
import tkinter as tk
from tkinter import ttk
import mysql.connector
from RegisterWindowGUI import RegisterView,RegisterController,RegisterApp
class ProjectSelectorView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.projectList = []
        self.pList = tk.Variable(value=self.projectList)
        #create widgets
        #label
        self.projectsLabel = ttk.Label(self, text = 'Choose a project')
        self.projectsLabel.grid(row = 0, columnspan=3)
        
        #list box
        self.projectListBox = tk.Listbox(
            self,
            listvariable = self.pList,
            height =30
        )
        self.projectListBox.grid(row = 1, columnspan=3, sticky = tk.NSEW)

        #remove project button
        self.removeProjectButton = ttk.Button(self, text = "  -  ", command=self.clickRemoveSelected)
        self.removeProjectButton.grid(row = 2, column = 1, padx=10,sticky = tk.NSEW)

        #button to add project
        self.addProjectButton = ttk.Button(self, text = "  +  ", command=self.clickAddProject)
        self.addProjectButton.grid(row = 2, column = 2, padx = 10,sticky = tk.NSEW)
        
        #button to see the info of a project
        self.seeInfoButton=ttk.Button(self, text="See Info", command =self.clickSeeInfo)
        self.seeInfoButton.grid(row=2, column=0, padx=10, sticky = tk.NSEW)

        #message 
        self.messageLabel = ttk.Label(self, text='', foreground='red')


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

    def clickRemoveSelected(self):
        if self.controller:
            self.controller.register()

    def clickAddProject(self):
        if self.controller:
            self.controller.register()

    def clickSeeInfo(self):
        if self.controller:
            self.controller.register()


class ProjectSelectorController:
    def __init__(self, view, user):
        self.view = view
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ch0keYourselfT0Sle#p"
        )
        mycursor = mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("Select `project_name` FROM Users U INNER JOIN projectmember PM ON U.`email` = PM.`member_email` WHERE U.`username` = '{}' ".format(user.getUsername()))
        projects= mycursor.fetchall()
        for i in projects:
            view.projectList.append(i[0])
        view.pList.set(view.projectList)


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
                mycursor.execute("SELECT `username`,`password`, `email`, `name` FROM Users WHERE `Username` = '{}'".format(i[0]))
                loginInfo = mycursor.fetchall()[0]
                loginUser = User(loginInfo[0], loginInfo[1], loginInfo[2], loginInfo[3])
                self.view.showMessage("Login Succedded")
                break
            else:
                self.view.showError("Invalid info")
    
    def register(self):
        self.registerWindow = RegisterApp()
class ProjectSelectorApp(tk.Tk):
    def __init__(self,user):
        super().__init__()
        
        self.title("Login")
        self.geometry("800x600")
        #create a view and place it on the root window
        view = ProjectSelectorView(self)
        view.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        view.rowconfigure(0, weight=1)
        view.columnconfigure(0, weight=1)
        #create the login controller
        controller = ProjectSelectorController(view,user)
        

        view.setController(controller)

if __name__ == '__main__':
    app = ProjectSelectorApp()
    app.mainloop()
