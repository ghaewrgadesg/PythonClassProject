from domains import Task, Project, User
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import askyesno, showerror
from tkcalendar import Calendar
import mysql.connector
from RegisterWindowGUI import RegisterView,RegisterController,RegisterApp
from TaskAdderGUI import TaskAdderApp, TaskAdderController, TaskAdderView

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
        self.taskListLabel.grid(row = 0,column = 0, sticky = tk.NSEW)

        #Sort task by start day
        self.taskCalendarButton = ttk.Button(self.listBoxFrame, text= "See calendar", command= self.clickSeeCalendar)
        self.taskCalendarButton.grid(row = 0, column = 2 )


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

        #renaming button
        self.taskNameButton = ttk.Button(self.listBoxFrame, text = 'Rename', command= self.clickChangeName)
        self.taskNameButton.grid(row = 2, column= 2, padx=10)

        #for info frame
        #Labels for start date and end date
        self.startDateLabel = ttk.Label(self.infoFrame,text= "Task's start date: ")
        self.startDateLabel.grid(row=0, column = 0)
        self.endDateLabel = ttk.Label(self.infoFrame,text= "Task's end date: ")
        self.endDateLabel.grid(row=1, column = 0)

        #button label for start date and end date
        self.startDateButton = ttk.Button(self.infoFrame,text= "", command= self.clickStartDate)
        self.endDateButton = ttk.Button(self.infoFrame,text= "", command = self.clickEndDate)

        #status box
        statusVar = tk.StringVar()
        self.statusLabel = ttk.Label(self.infoFrame, text= "Status")
        self.statusLabel.grid(row= 2, column= 0)
        self.statusComboBox = ttk.Combobox(self.infoFrame, textvariable= statusVar, state = 'readonly')
        self.statusComboBox['values'] = ('NOT STARTED', 'IN PROGRESS', 'FINISHED')
        self.statusComboBox.bind('<<ComboboxSelected>>', self.clickStatusChange)


        #description text box
        self.taskDescriptionBox = ScrolledText(self.infoFrame, height = 20, width=30)
        self.taskDescriptionBox.grid(row=3, column = 0, columnspan=2, pady = 5)
     

        #member list box
        self.memberListBox = tk.Listbox(
            self.infoFrame,
            listvariable = self.mList,
            height =15,width= 40
        )
        self.memberListBox.grid(row=4, column = 0, columnspan=2 , pady = 5)
        
        #Add member and remove member buttons
        self.addMemberButton = ttk.Button(self.infoFrame, text= " + ", command= self.clickAddMember)
        self.addMemberButton.grid(row = 5,column=0)
        self.removeMemberButton = ttk.Button(self.infoFrame, text= " - ", command = self.clickRemoveMember)
        self.removeMemberButton.grid(row= 5, column= 1)

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
    
    def clickStatusChange(self, event):
        if self.controller:
            self.controller.changeStatus()

    def clickChangeName(self):
        if self.controller:
            self.controller.changeName()

    def clickStartDate(self):
        if self.controller:
            self.controller.pickStartDate(self)

    def clickEndDate(self):
        if self.controller:
            self.controller.pickEndDate(self)

    def clickAddMember(self):
        if self.controller:
            self.controller.addMember()

    def clickRemoveMember(self):
        if self.controller:
            self.controller.removeMember()

    def clickSeeCalendar(self):
        if self.controller:
            self.controller.seeTaskCalendar()

class TaskWindowController:
    def __init__(self, view, app):
        with open("databasePassword.txt") as f:
            databasePassword = f.readline().rstrip()
        self.view = view
        self.app = app
        self.toBeChecked =''
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password = databasePassword
        )
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("select `name` from `Tasks` where `project_name` = '{}' ORDER BY `start_date` ASC".format(app.project.getName()))
        tasks= mycursor.fetchall()
        for i in tasks:
            view.taskList.append(i[0])
        view.tList.set(view.taskList)
        if self.app.user.getEmail() != self.app.project.getManagerEmail():
                self.view.addMemberButton.grid_remove()
                self.view.removeMemberButton.grid_remove()
                self.view.taskNameButton.grid_remove()
                self.view.addTaskButton.grid_remove()
                self.view.removeTaskButton.grid_remove()

    def login(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("SELECT `username`, `password` FROM Users")
        loginInfo = mycursor.fetchall()
    
    def refreshTaskList(self):
        self.mydb.reconnect(attempts=1, delay=0)
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("select `name` from `Tasks` where `project_name` = '{}' ORDER BY `start_date` ASC".format(self.app.project.getName()))
        tasks= mycursor.fetchall()
        self.view.taskList = []
        for i in tasks:
            self.view.taskList.append(i[0])
        self.view.tList.set(self.view.taskList)
    
    def addTask(self):
        taskAdderWindow = TaskAdderApp(self.app.project.getName())
        self.app.wait_window(taskAdderWindow)
        self.refreshTaskList()

    def removeTask(self):
        answer = askyesno(title = "Are you sure?", message= "Are you sure you want to delete this task and all its data forever")
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
        self.mydb.reconnect(attempts=1, delay=0)
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        currentSelection = self.view.taskListBox.curselection()
        try:
            self.toBeChecked = self.view.taskListBox.get(currentSelection[0])
            mycursor.execute("SELECT `name`, `start_date`, `end_date`, `description`, `status` FROM `tasks` WHERE (`name` = '{}' AND `project_name` = '{}');".format(self.toBeChecked,self.app.project.getName()))
            taskInfo = mycursor.fetchall()[0]
            self.view.startDateButton.grid(row=0, column = 1)
            self.view.endDateButton.grid(row=1, column = 1)
            self.view.startDateButton['text']= "{}".format(taskInfo[1])
            self.view.endDateButton['text']= "{}".format(taskInfo[2])
            self.view.statusComboBox.grid(row= 2, column= 1)
            self.view.statusComboBox.set(taskInfo[4])
            if taskInfo[3] != None:
                self.view.taskDescriptionBox['state'] = 'normal'
                self.view.taskDescriptionBox.delete('1.0', tk.END)
                self.view.taskDescriptionBox.insert('1.0',taskInfo[3])
            else:
                self.view.taskDescriptionBox['state'] = 'normal'
                self.view.taskDescriptionBox.delete('1.0', tk.END)
                self.view.taskDescriptionBox['state'] = 'disabled'

            mycursor.execute("select `member_email` from `AssignedTaskMember` where (`task_name` = '{}') AND (`project_name` = '{}'); ".format(self.toBeChecked, self.app.project.getName()))
            members = mycursor.fetchall()
            self.view.memberList = []
            for i in members:
                self.view.memberList.append(i[0])
            self.view.mList.set(self.view.memberList)
            mycursor.execute("SELECT `name`, `start_date`, `end_date`,`status`, `description`, `cost` FROM `tasks` WHERE (`name` = '{}' AND `project_name` = '{}');".format(self.toBeChecked,self.app.project.getName()))
            taskInfo = mycursor.fetchall()[0]
            self.selectedTask = Task(taskInfo[0],taskInfo[1], taskInfo[2], taskInfo[3], taskInfo[4], taskInfo[5])
            for i in members:
                self.selectedTask.getMemList().append(i[0])
            #UI changes if not manager
            if self.app.user.getEmail() != self.app.project.getManagerEmail():
                self.view.taskDescriptionBox['state'] = 'disabled'
                self.view.startDateButton['state'] = 'disabled'
                self.view.endDateButton['state'] = 'disabled'
        except IndexError:
            pass

    def refreshSelectedInfo(self):
        self.mydb.reconnect(attempts=1, delay=0)
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        try:
            mycursor.execute("SELECT `name`, `start_date`, `end_date`, `description`, `status` FROM `tasks` WHERE (`name` = '{}' AND `project_name` = '{}');".format(self.toBeChecked,self.app.project.getName()))
            taskInfo = mycursor.fetchall()[0]
            self.view.startDateButton.grid(row=0, column = 1)
            self.view.endDateButton.grid(row=1, column = 1)
            self.view.startDateButton['text']= "{}".format(taskInfo[1])
            self.view.endDateButton['text']= "{}".format(taskInfo[2])
            self.view.statusComboBox.grid(row= 2, column= 1)
            self.view.statusComboBox.set(taskInfo[4])
            if taskInfo[3] != None:
                self.view.taskDescriptionBox['state'] = 'normal'
                self.view.taskDescriptionBox.delete('1.0', tk.END)
                self.view.taskDescriptionBox.insert('1.0',taskInfo[3])
            else:
                self.view.taskDescriptionBox['state'] = 'normal'
                self.view.taskDescriptionBox.delete('1.0', tk.END)
                self.view.taskDescriptionBox['state'] = 'disabled'

            mycursor.execute("select `member_email` from `AssignedTaskMember` where (`task_name` = '{}') AND (`project_name` = '{}'); ".format(self.toBeChecked, self.app.project.getName()))
            members = mycursor.fetchall()
            self.view.memberList = []
            for i in members:
                self.view.memberList.append(i[0])
            self.view.mList.set(self.view.memberList)
            mycursor.execute("SELECT `name`, `start_date`, `end_date`,`status`, `description`, `cost` FROM `tasks` WHERE (`name` = '{}' AND `project_name` = '{}');".format(self.toBeChecked,self.app.project.getName()))
            taskInfo = mycursor.fetchall()[0]
            self.selectedTask = Task(taskInfo[0],taskInfo[1], taskInfo[2], taskInfo[3], taskInfo[4], taskInfo[5])
        except IndexError:
            pass

    def changeStatus(self):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("USE InformationManagementSystem;")
            mycursor.execute("SELECT `name`, `start_date`, `end_date`, `description`, `cost` FROM `tasks` WHERE (`name` = '{}' AND `project_name` = '{}');".format(self.toBeChecked,self.app.project.getName()))
            taskInfo = mycursor.fetchall()[0]
            test = Task(taskInfo[0],taskInfo[1], taskInfo[2], self.view.statusComboBox.get(), taskInfo[3], taskInfo[4])
            test.update(self.app.project.getName())
        except ValueError:
            pass
    
    def changeName(self):
        changeNameWindow = tk.Toplevel()

        changeNameFrame = ttk.Frame(changeNameWindow)
        changeNameFrame.grid(row= 0, column= 0, padx =10, pady= 10)
        
        #Search box entry
        nameEntry = ttk.Entry(changeNameFrame, width = 30)
        nameEntry.grid(row = 0, column= 0)

        #Message in case of error
        messageLabel = ttk.Label(changeNameFrame, text='', foreground='red')
        messageLabel.grid(row=2, column=0, sticky=tk.W)

        def showError(message):
            messageLabel['text'] = message
            messageLabel['foreground'] = 'red'
            

        def changeName():
                newName = nameEntry.get()
                try:
                    mycursor = self.mydb.cursor()
                    mycursor.execute("USE InformationManagementSystem;")
                    mycursor.execute("SELECT `name`, `start_date`, `end_date`,`status`, `description`, `cost` FROM `tasks` WHERE (`name` = '{}' AND `project_name` = '{}');".format(self.toBeChecked,self.app.project.getName()))
                    taskInfo = mycursor.fetchall()[0]
                    print(self.view.statusComboBox.get())
                    test = Task(taskInfo[0],taskInfo[1], taskInfo[2], taskInfo[3], taskInfo[4], taskInfo[5])
                    test.updateName(self.app.project.getName(),newName)
                    self.refreshTaskList()
                    changeNameWindow.destroy()
                except mysql.connector.IntegrityError:
                    showError("There's already a task with that name")


        #Name change button
        changeNameButton = ttk.Button(changeNameFrame, text="Change Name", command=changeName)
        changeNameButton.grid(row=1, column= 0, padx=5, pady=5)

    def pickStartDate(self, view):
        root = tk.Toplevel()
 
        # Set geometry
        todayDate = self.selectedTask.getStartDate().strftime('%Y-%m-%d').split('-')
        # Add Calendar
        cal = Calendar(root, selectmode = 'day',
                    year = int(todayDate[0]), month = int(todayDate[1]),
                    day = int(todayDate[2]), date_pattern = 'yyyy-mm-dd')
        
        cal.grid(row = 0)
        
        def getDate():
            view.startDateButton['text']= cal.get_date()
            self.selectedTask.setStartDate(datetime.strptime(cal.get_date(),'%Y-%m-%d'))
            self.selectedTask.update(self.app.project.getName())
            root.destroy()
        
        # Add Button and Label
        getSelectedDateButton = ttk.Button(root, text = "Get Date",command = getDate)
        getSelectedDateButton.grid(row =1)

    def pickEndDate(self, view):
        root = tk.Toplevel()
 
        # Set geometry
        todayDate = self.selectedTask.getEndDate().strftime('%Y-%m-%d').split('-')
        # Add Calendar
        cal = Calendar(root, selectmode = 'day',
                    year = int(todayDate[0]), month = int(todayDate[1]),
                    day = int(todayDate[2]), date_pattern = 'yyyy-mm-dd')
        
        cal.grid(row = 0)
        
        def getDate():
            if datetime.strptime(cal.get_date(),'%Y-%m-%d').date() > datetime.strptime(view.startDateButton['text'],'%Y-%m-%d').date():
                view.endDateButton['text']= cal.get_date()
                self.selectedTask.setEndDate(datetime.strptime(cal.get_date(),'%Y-%m-%d'))
                self.selectedTask.update(self.app.project.getName())
                self.mydb.reconnect(attempts=1, delay=0)
                root.destroy()
            else:
                showerror('Wrong date', 'End date cannot be earlier than start date')
        # Add Button and Label
        getSelectedDateButton = ttk.Button(root, text = "Get Date",command = getDate)
        getSelectedDateButton.grid(row =1)

    def addMember(self):
        if self.toBeChecked:
            addMemberWindow = tk.Toplevel()

            addMemberFrame = ttk.Frame(addMemberWindow)
            addMemberFrame.grid(row= 0, column= 0, padx =10, pady= 10)
            
            #Search box entry
            searchEntry = ttk.Entry(addMemberFrame, width = 30)
            searchEntry.grid(row = 0, column= 0)


            #Listbox for the members
            memberVar = tk.StringVar()
            memberBox = tk.Listbox(addMemberFrame, width= 30, listvariable= memberVar)
            memberBox.grid(row = 1, column = 0, pady =5)
            mycursor = self.mydb.cursor()
            mycursor.execute("USE InformationManagementSystem;")
            mycursor.execute("SELECT `member_email` FROM `projectMember` WHERE `project_name` = '{}' AND `member_email` NOT IN (select `member_email` from `AssignedTaskMember`" 
                        " WHERE `project_name` = '{}' AND `task_name` = '{}');".format(self.app.project.getName(), self.app.project.getName(),self.selectedTask.getName()))
            memberList = mycursor.fetchall()
            if memberList == []:
                addMemberWindow.destroy()
                print("No more member to add")
                return
            memberVar.set(memberList)
            def Scankey(event):
                
                val = event.widget.get()
                

                if val == '':
                    data = memberList
                else:
                    data = []
                    for item in memberList:
                        if val.lower() in item[0].lower():
                            data.append(item)				

                
                update(data)
            
            def update(data):
                memberVar.set(data)

            def chooseMember(event):
                currentSelection = memberBox.curselection()
                toBeChecked = memberBox.get(currentSelection[0])
                mycursor = self.mydb.cursor()
                mycursor.execute("USE InformationManagementSystem;")
                mycursor.execute("SELECT `member_email` FROM `projectMember` WHERE `project_name` = '{}' AND `member_email` NOT IN (select `member_email` from `AssignedTaskMember`" 
                        " WHERE `project_name` = '{}' AND `task_name` = '{}');".format(self.app.project.getName(), self.app.project.getName(),self.selectedTask.getName()))
                memberList = mycursor.fetchall()
                memberList.remove(toBeChecked)
                memberVar.set(memberList)
                mycursor.execute("SELECT `email` FROM `users` WHERE `email` = '{}';".format(toBeChecked[0]))
                tMemberList = mycursor.fetchall()[0]
                self.selectedTask.getMemList().append(tMemberList)
                self.selectedTask.update(self.app.project.getName())
                self.refreshSelectedInfo()


            #Bind the search function
            searchEntry.bind('<KeyRelease>', Scankey)
            #bind double click action to listbox
            memberBox.bind('<Double-1>', chooseMember)
        else:
            print("No task selected")
    
    def removeMember(self):
        currentSelection = self.view.memberListBox.curselection()
        currentItem = self.view.memberListBox.get(currentSelection[0])
        self.selectedTask.getMemList().remove(currentItem)
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("DELETE FROM `AssignedTaskMember` WHERE (`member_email` = '{}') and (`project_name` = '{}') AND (`task_name` = '{}');".format(currentItem, self.app.project.getName(), self.selectedTask.getName()))
        self.mydb.commit()
        self.refreshSelectedInfo()

    def seeTaskCalendar(self):
        taskCalendarWindow = tk.Toplevel()

        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("SELECT `start_date`, `name` FROM `tasks` WHERE (`project_name` = '{}');".format(self.app.project.getName()))
        events = mycursor.fetchall()
        cal = Calendar(taskCalendarWindow, selectmode='day', date_pattern = 'yyyy-mm-dd')
        print(events)

        for k in events:
            cal.calevent_create(k[0], k[1], 'task')

        cal.tag_config('task', background='red', foreground='yellow')
        cal.pack(fill="both", expand=True)

        def getEventOfDate(event):
            eventIds = cal.get_calevents(datetime.strptime(cal.get_date(),"%Y-%m-%d").date())
            taskList =[]
            for i in eventIds:
                taskName = cal.calevent_cget(i,'text')
                taskList.append(taskName)
            self.view.tList.set(taskList)

        def onClose():
            self.refreshTaskList()
            taskCalendarWindow.destroy()

        cal.bind('<<CalendarSelected>>',getEventOfDate)
        taskCalendarWindow.protocol('WM_DELETE_WINDOW',onClose)

        


class TaskWindowApp(tk.Tk):
    def __init__(self, user, project):
        super().__init__()
        self.project = project
        self.user = user
        self.title("Task Window")

        #create a view and place it on the root window
        view = TaskWindowView(self)
        view.grid(row = 0, column = 0, padx = 10, pady = 10)

        #create the login controller
        controller = TaskWindowController(view,self)

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
    app = TaskWindowApp(loginUser,chosenProject)
    app.mainloop()
