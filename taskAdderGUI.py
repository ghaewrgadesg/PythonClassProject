from domains import Task, Task, User
import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter.messagebox import showerror
from datetime import date, datetime
from tkcalendar import Calendar
from tkinter.scrolledtext import ScrolledText
class TaskAdderView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        #Create widgets
        #labels
        self.nameLabel = ttk.Label(self, text="Task name")
        self.nameLabel.grid(row= 0, column= 0, columnspan= 2)
        self.startDateLabel = ttk.Label(self, text= "Start Date")
        self.startDateLabel.grid(row = 2, column = 0, columnspan= 2)
        self.endDateLabel = ttk.Label(self, text= "End Date")
        self.endDateLabel.grid(row = 4, column= 0, columnspan= 2)
        self.costLabel = ttk.Label(self, text="Cost")
        self.costLabel.grid(row = 6, column = 0, columnspan=2)
        self.descriptionLabel = ttk.Label(self, text= "Description")
        self.descriptionLabel.grid(row = 8, column = 0, columnspan= 2)

        #Textbox
        self.pNameVar = tk.StringVar()
        self.costVar = tk.StringVar()
        self.nameEntry = ttk.Entry(self, textvariable=self.pNameVar, width = 40)
        self.nameEntry.grid(row = 1, columnspan=2)

        #Button to open the calendar and choose a date
        self.startDateButton = ttk.Button(self, text= "Choose a date", command= self.clickStartDate)
        self.startDateButton.grid(row = 3, column = 0, columnspan= 2)
        self.endDateButton = ttk.Button(self, text= "Choose a date", command = self.clickEndDate)
        self.endDateButton.grid(row = 5, column = 0, columnspan= 2)

        #more textbox
        self.costEntry = ttk.Entry(self, textvariable=self.costVar, width = 40)
        self.costEntry.grid(row = 7, columnspan= 2)

        #Description textbox
        self.description = ScrolledText(self, width=50, height=10)
        self.description.grid(row = 9, columnspan= 2)

        #Buttons to create the Task and to cancel
        self.createTaskButton = ttk.Button(self, text= "Create the Task", command= self.clickCreateTask)
        self.createTaskButton.grid(row = 10, column = 0)
        self.cancelButton = ttk.Button(self, text= "Cancel", command= self.clickCancel)
        self.cancelButton.grid(row=10, column = 1)


        #message 
        self.messageLabel = ttk.Label(self, text='', foreground='red')
        self.messageLabel.grid(row=11, columnspan=2)

        #set the controller
        self.controller = None
    
    def setController(self, controller):
        self.controller = controller

    def hideMessage(self):
        """
        Hide the message
        :return:
        """
        self.messageLabel['text'] = ''

    def showError(self, message):
        self.messageLabel['text'] = message
        self.messageLabel['foreground'] = 'red'
        self.messageLabel.after(3000, self.hideMessage)
 
    def showMessage(self, message):
        self.messageLabel['text'] = message
        self.messageLabel['foreground'] = 'green'
        self.messageLabel.after(3000, self.hideMessage)


    def clickStartDate(self):
        if self.controller:
            self.controller.pickStartDate(self)

    def clickEndDate(self):
        if self.controller:
            self.controller.pickEndDate(self)

    def clickCancel(self):
        if self.controller:
            self.controller.cancel()
    
    def clickCreateTask(self):
        if self.controller:
            self.controller.createTask(self.pNameVar.get(), self.startDateButton['text'], self.endDateButton['text'], self.costVar.get(), self.description.get('1.0', 'end'))

    
class TaskAdderController:
    def __init__(self, view, app):
        self.view = view
        self.app = app
    
    def pickStartDate(self, view):
        root = tk.Toplevel()
 
        # Set geometry
        todayDate = date.today()
        # Add Calendar
        cal = Calendar(root, selectmode = 'day',
                    year = todayDate.year, month = todayDate.month,
                    day = todayDate.day, date_pattern = 'yyyy-mm-dd')
        
        cal.grid(row = 0)
        
        def getDate():
            view.startDateButton['text']= cal.get_date()
            root.destroy()
        
        # Add Button and Label
        getSelectedDateButton = ttk.Button(root, text = "Get Date",command = getDate)
        getSelectedDateButton.grid(row =1)

    #literally a duplicate of the one above
    def pickEndDate(self, view):
        root = tk.Toplevel()
 
        # Set geometry
        todayDate = date.today()
        # Add Calendar
        cal = Calendar(root, selectmode = 'day',
                    year = todayDate.year, month = todayDate.month,
                    day = todayDate.day, date_pattern = 'yyyy-mm-dd')
        
        cal.grid(row = 0)
        
        def getDate():
            if datetime.strptime(cal.get_date(),'%Y-%m-%d').date() > datetime.strptime(view.startDateButton['text'],'%Y-%m-%d').date():
                view.endDateButton['text']= cal.get_date()
                root.destroy()
            else:
                showerror('Wrong date', 'End date cannot be earlier than start date')
            
        
        # Add Button and Label
        getSelectedDateButton = ttk.Button(root, text = "Get Date",command = getDate)
        getSelectedDateButton.grid(row =1)

    def cancel(self):
        self.app.destroy()

    def createTask(self, taskName, startDate, endDate, cost, description):
        try:
            test = Task(taskName, startDate, endDate, 'NOT STARTED', description, int(cost))
            test.save(self.app.projectName)
            self.app.destroy()
        except ValueError as error:
            self.view.showError(error)

class TaskAdderApp(tk.Toplevel):
    def __init__(self, projectName):
        super().__init__()
        self.projectName = projectName
        #create a view and place it on the root window
        view = TaskAdderView(self)
        view.grid(row = 0, column = 0, padx = 10, pady = 10)

        #create the login controller
        controller = TaskAdderController(view,self)

        view.setController(controller)
if __name__ == '__main__':
    global databasePassword
    with open("databasePassword.txt") as f:
        databasePassword = f.readline().rstrip()
    app = TaskAdderApp()
    app.mainloop()



    