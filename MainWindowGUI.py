from domains import Task, Project, User
import tkinter as tk
from tkinter import ttk
import mysql.connector
from TaskWindowGUI import TaskWindowApp, TaskWindowController, TaskWindowView
from ProjectInfoGUI import ProjectInfoWindowApp, ProjectInfoWindowController, ProjectInfoWindowView
class MainWindowView(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        #create widgets
        #Notebook Windows
        self.projectInfoWindow = ProjectInfoWindowView(self)
        self.projectInfoWindow.pack(fill = 'both', expand=True)
        self.add(self.projectInfoWindow, text= 'Project Info')
        
        self.taskWindow = TaskWindowView(self)
        self.taskWindow.pack(fill = 'both', expand=True)
        self.add(self.taskWindow, text= 'Tasks')
        
        #set the controller
        self.controller = None
        self.bind('<<NotebookTabChanged>>',self.onTabChange)
    
    def setController(self, controller):
        self.controller = controller

    def clickMainWindow(self):
        if self.controller:
            self.controller.MainWindow(self.usernameVar.get(), self.passwordVar.get())
    
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
    
    def onTabChange(self,event):
        if self.controller:
            self.controller.onTabChanged(event)


class MainWindowController:
    def __init__(self, view, app):
        self.view = view
        self.app = app
    
    def onTabChanged(self,event):
        tab = event.widget.tab('current')['text']
        if tab == 'Project Info':
            self.view.projectInfoWindow.refreshSelfInfo()



class MainWindowApp(tk.Tk):
    def __init__(self, user, project):
        super().__init__()
        self.user = user
        self.project = project
        self.title("MainWindow")

        #create a view and place it on the root window
        view = MainWindowView(self)
        view.grid(row = 0, column = 0, padx = 10, pady = 10)


        #create the taskWindow controller
        taskWindowControl = TaskWindowController(view.taskWindow, self)
        view.taskWindow.setController(taskWindowControl)
        
        #create the projectInfo controller
        projectInfoControl = ProjectInfoWindowController(view.projectInfoWindow,self)
        view.projectInfoWindow.setController(projectInfoControl)


        #create the MainWindow controller
        controller = MainWindowController(view,self)

        view.setController(controller)
if __name__ == '__main__':
    with open("databasePassword.txt") as f:
        databasePassword = f.readline().rstrip()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=databasePassword
        )
    mycursor = mydb.cursor()
    mycursor.execute("USE InformationManagementSystem;")
    mycursor.execute("SELECT `username`,`password`, `email`, `name` FROM Users WHERE `Username` = 'bthung2003';")
    loginInfo = mycursor.fetchall()[0]
    loginUser = User(loginInfo[0], loginInfo[1], loginInfo[2], loginInfo[3])
    mycursor.execute("SELECT `name`,`manager_email`, `start_date`, `end_date`, `description` FROM `Project` WHERE (`name` = 'Killing the world');")
    projectInfo = mycursor.fetchall()[0]
    mycursor.execute("SELECT `potential_budget`, `plan_budget` FROM `ProjectBudget` WHERE (`project_name` = 'Killing the world');")
    projectBudgetInfo = mycursor.fetchall()[0]
    chosenProject = Project(projectInfo[0],projectInfo[1],projectInfo[2], projectInfo[3],projectBudgetInfo[0],projectBudgetInfo[1],projectInfo[4])
    app = MainWindowApp(loginUser,chosenProject)
    app.mainloop()
