from domains import Task, Project, User
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import askyesno
import mysql.connector
from RegisterWindowGUI import RegisterView,RegisterController,RegisterApp
from ProjectSelectorGUI import ProjectSelectorView, ProjectSelectorController, ProjectSelectorApp
from taskAdderGUI import TaskAdderApp, TaskAdderController, TaskAdderView
class TaskWindowView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.taskList = []
        self.tList = tk.Variable(value=self.taskList)
        self.memberList = []
        self.mList = tk.Variable(value= self.memberList)
        #create widgets
        #2 frames side by side
        self.listBoxFrame = ttk.Frame(self)
        self.listBoxFrame.grid(row = 0, column = 0, padx=10, pady=10)
        self.infoFrame = ttk.Frame(self)
        self.infoFrame.grid(row= 0, column = 1, padx=10, pady= 10)
        
        #For listbox Frame
        #Label for tasks
        self.taskListLabel = ttk.Label(self.listBoxFrame, text= "Task List")
        self.taskListLabel.grid(row = 0, sticky = tk.NSEW)

        #listbox
        self.taskListBox = tk.Listbox(
            self.listBoxFrame,
            listvariable = self.tList,
            height =30,width=50
        )
        self.taskListBox.grid(row = 1, columnspan=3, sticky = tk.NSEW)
        
        self.taskListBox.bind('<<ListboxSelect>>', self.clickShowSelectedInfo)


        #Buttons for adding and removing tasks
        self.removeTaskButton = ttk.Button(self.listBoxFrame, text = "  -  ", command= self.clickRemoveTask)
        self.removeTaskButton.grid(row = 2, column = 0, padx=10)
        self.addTaskButton = ttk.Button(self.listBoxFrame, text = "  +  ", command = self.clickAddTask)
        self.addTaskButton.grid(row = 2, column = 1, padx = 10)

        #for info frame
        #label for start date and end date
        self.startDateLabel = ttk.Label(self.infoFrame,text= "Task's start date: ")
        self.startDateLabel.grid(row=0, column = 0)
        self.endDateLabel = ttk.Label(self.infoFrame,text= "Task's end date: ")
        self.endDateLabel.grid(row=1, column = 0)

        #description text box
        self.taskDescriptionBox = ScrolledText(self.infoFrame, height = 20, width=30, state= 'disabled')
        self.taskDescriptionBox.grid(row=2, column = 0, pady = 5)
     

        #member list box
        self.memberListBox = tk.Listbox(
            self.infoFrame,
            listvariable = self.mList,
            height =15,width= 40
        )
        self.memberListBox.grid(row=3, column = 0, pady = 5)
        
        #set the controller
        self.controller = None

    def setController(self, controller):
        self.controller = controller

    def clickLogin(self):
        if self.controller:
            self.controller.login()
    
    def clickAddTask(self):
        if self.controller:
            self.controller.addTask()

    def clickRemoveTask(self):
        if self.controller:
            self.controller.removeTask()

    def clickShowSelectedInfo(self, event):
            if self.controller:
                self.controller.showSelectedInfo()
    
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

    


class TaskWindowController:
    def __init__(self, view, app):
        with open("databasePassword.txt") as f:
            databasePassword = f.readline().rstrip()
        self.view = view
        self.app = app
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password = databasePassword
        )
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("select `name` from `Tasks` where `project_name` = '{}' ORDER BY `start_date` ASC".format(app.projectName))
        tasks= mycursor.fetchall()
        for i in tasks:
            view.taskList.append(i[0])
        view.tList.set(view.taskList)

    def login(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("SELECT `username`, `password` FROM Users")
        loginInfo = mycursor.fetchall()
    
    def refreshTaskList(self):
        self.mydb.reconnect(attempts=1, delay=0)
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("select `name` from `Tasks` where `project_name` = '{}' ORDER BY `start_date` ASC".format(self.app.projectName))
        tasks= mycursor.fetchall()
        self.view.taskList = []
        print(self.view.taskList)
        print(tasks)
        for i in tasks:
            self.view.taskList.append(i[0])
        print(self.view.taskList)
        self.view.tList.set(self.view.taskList)
    
    def addTask(self):
        taskAdderWindow = TaskAdderApp(self.app.projectName)
        print("STOP")
        self.app.wait_window(taskAdderWindow)
        self.refreshTaskList()

    def removeTask(self):
        answer = askyesno(title = "Are you sure?", message= "Are you sure you want to delete this project and all its data forever")
        if answer:
            mycursor = self.mydb.cursor()
            mycursor.execute("USE InformationManagementSystem;")
            currentSelection = self.view.taskListBox.curselection()
            toBeDeleted = self.view.taskListBox.get(currentSelection[0])
            mycursor.execute("DELETE FROM `informationmanagementsystem`.`Tasks` WHERE (`name` = '{}');".format(toBeDeleted))
            self.mydb.commit()
            self.refreshTaskList()
        
    #show the info of the selected task
    def showSelectedInfo(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        currentSelection = self.view.taskListBox.curselection()
        toBeChecked = self.view.taskListBox.get(currentSelection[0])
        mycursor.execute("SELECT `name`, `start_date`, `end_date`, `description` FROM `tasks` WHERE (`name` = '{}');".format(toBeChecked))
        taskInfo = mycursor.fetchall()[0]
        self.view.startDateLabel['text']= "Task's start date: {}".format(taskInfo[1])
        self.view.endDateLabel['text']= "Task's end date: {}".format(taskInfo[2])
        if taskInfo[3] != None:
            self.view.taskDescriptionBox['state'] = 'normal'
            self.view.taskDescriptionBox.delete('1.0', tk.END)
            self.view.taskDescriptionBox.insert('1.0',taskInfo[3])
            self.view.taskDescriptionBox['state'] = 'disabled'
        else:
            self.view.taskDescriptionBox['state'] = 'normal'
            self.view.taskDescriptionBox.delete('1.0', tk.END)
            self.view.taskDescriptionBox['state'] = 'disabled'

        mycursor.execute("select `member_email` from `AssignedTaskMember` where (`task_name` = '{}') AND (`project_name` = '{}'); ".format(toBeChecked, app.projectName))
        members = mycursor.fetchall()
        self.view.memberList = []
        for i in members:
            self.view.memberList.append(i[0])
        self.view.mList.set(self.view.memberList)

    



class TaskWindowApp(tk.Tk):
    def __init__(self, projectName):
        super().__init__()
        self.projectName = projectName
        self.title("Login")

        #create a view and place it on the root window
        view = TaskWindowView(self)
        view.grid(row = 0, column = 0, padx = 10, pady = 10)

        #create the login controller
        controller = TaskWindowController(view,self)

        view.setController(controller)

if __name__ == '__main__':
    app = TaskWindowApp('Killing the world')
    app.mainloop()
