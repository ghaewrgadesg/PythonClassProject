from domains import Task, Project, User
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showerror
import datetime
import mysql.connector
from RegisterWindowGUI import RegisterView,RegisterController,RegisterApp
from ProjectAdder import ProjectAdderApp, ProjectAdderController, ProjectAdderView
from MainWindowGUI import MainWindowApp, MainWindowController, MainWindowView

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

        #bind double click action to listbox
        self.projectListBox.bind('<Double-1>', self.clickTwiceChooseProject)


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
            self.controller.removeSelected()

    def clickAddProject(self):
        if self.controller:
            self.controller.addProject()

    def clickSeeInfo(self):
        if self.controller:
            self.controller.seeInfo()

    def clickTwiceChooseProject(self, event):
        if self.controller:
            self.controller.chooseProject()

class ProjectSelectorController:
    def __init__(self, view, app):
        with open("databasePassword.txt") as f:
            databasePassword = f.readline().rstrip()
        self.view = view
        self.app = app
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=databasePassword
        )
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("Select `project_name` FROM Users U INNER JOIN projectmember PM ON U.`email` = PM.`member_email` WHERE U.`username` = '{}' ".format(app.user.getUsername()))
        projects= mycursor.fetchall()
        for i in projects:
            view.projectList.append(i[0])
        view.pList.set(view.projectList)

    def refreshProjectList(self):
        self.mydb.reconnect(attempts=1, delay=0)
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("Select `project_name` FROM Users U INNER JOIN projectmember PM ON U.`email` = PM.`member_email` WHERE U.`username` = '{}' ".format(self.app.user.getUsername()))
        projects= mycursor.fetchall()
        self.view.projectList = []
        for i in projects:
            self.view.projectList.append(i[0])
        self.view.pList.set(self.view.projectList)
    
    def addProject(self):
        projectAdderWindow = ProjectAdderApp(self.app.user)
        self.app.wait_window(projectAdderWindow)
        self.refreshProjectList()

    def removeSelected(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        currentSelection = self.view.projectListBox.curselection()
        toBeDeleted = self.view.projectListBox.get(currentSelection[0])
        mycursor.execute("SELECT `manager_email` FROM `Project` where `name` = '{}'".format(toBeDeleted))
        managerEmail = mycursor.fetchall()[0]
        if managerEmail == self.app.user.getEmail():
            answer = askyesno(title = "Are you sure?", message= "Are you sure you want to delete this project and all its data forever")
            if answer:
                mycursor.execute("DELETE FROM `informationmanagementsystem`.`Project` WHERE (`name` = '{}');".format(toBeDeleted))
                self.mydb.commit()
                self.refreshProjectList()
        else:
            showerror(
            title='Error',
            message='You are not the manager of this project')



    def seeInfo(self):
        popup = tk.Toplevel()
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        currentSelection = self.view.projectListBox.curselection()
        toBeChecked = self.view.projectListBox.get(currentSelection[0])
        mycursor.execute("SELECT `name`, `start_date`, `end_date`, `description` FROM `Project` WHERE (`name` = '{}');".format(toBeChecked))
        projectInfo = mycursor.fetchall()[0]
        #Labels for project's duration
        startDateLabel = ttk.Label(popup,text= "Project's start date: {}".format(projectInfo[1].strftime("%Y-%m-%d")))
        startDateLabel.grid(row=0)
        endDateLabel = ttk.Label(popup,text= "Project's end date: {}".format(projectInfo[2].strftime("%Y-%m-%d")))
        endDateLabel.grid(row=1)
        
        #textbox 
        descriptionText= ScrolledText(popup, width = 50, height = 10)
        descriptionText.grid(row= 2, padx=10, pady=10)
        descriptionText.insert('1.0',projectInfo[3])
        descriptionText['state'] = 'disabled'
    
    def chooseProject(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        currentSelection = self.view.projectListBox.curselection()
        toBeChecked = self.view.projectListBox.get(currentSelection[0])
        mycursor.execute("SELECT `name`,`manager_email`, `start_date`, `end_date`, `description` FROM `Project` WHERE (`name` = '{}');".format(toBeChecked))
        projectInfo = mycursor.fetchall()[0]
        mycursor.execute("SELECT `potential_budget`, `plan_budget` FROM `ProjectBudget` WHERE (`project_name` = '{}');".format(toBeChecked))
        projectBudgetInfo = mycursor.fetchall()[0]
        chosenProject = Project(projectInfo[0],projectInfo[1],projectInfo[2], projectInfo[3],projectBudgetInfo[0],projectBudgetInfo[1],projectInfo[4])
        mainWindow = MainWindowApp(self.app.user,chosenProject)
        mainWindow.mainloop()

class ProjectSelectorApp(tk.Tk):
    def __init__(self,user):
        super().__init__()
        self.user = user
        self.title("Select a project")
        self.geometry("800x600")
        #create a view and place it on the root window
        view = ProjectSelectorView(self)
        view.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        view.rowconfigure(0, weight=1)
        view.columnconfigure(0, weight=1)
        #create the login controller
        controller = ProjectSelectorController(view,self)
        

        view.setController(controller)

if __name__ == '__main__':
    app = ProjectSelectorApp()
    app.mainloop()
