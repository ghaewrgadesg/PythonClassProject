from domains import Task, Project, User
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import askyesno
from tkcalendar import Calendar
from datetime import date, datetime
import mysql.connector
from RegisterWindowGUI import RegisterView,RegisterController,RegisterApp
from TaskAdderGUI import TaskAdderApp, TaskAdderController, TaskAdderView
class ProjectInfoWindowView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.taskList = []
        self.tList = tk.Variable(value=self.taskList)
        self.memberList = []
        self.mList = tk.Variable(value= self.memberList)
        #create widgets
        #frames side by side
        self.projectFrame = ttk.Frame(self)
        self.projectFrame.grid(row = 0, column = 0, rowspan=2, padx=10, pady=10)
        self.budgetFrame = ttk.Frame(self)
        self.budgetFrame.grid(row= 0, column = 1, padx=10, pady= 10)
        self.memberFrame = ttk.Frame(self)
        self.memberFrame.grid(row= 1, column= 1, padx=10,pady=10)

        #for the projectFrame
        #labels
        self.nameLabel = ttk.Label(self.projectFrame, text= 'Name: ')
        self.nameLabel.grid(row = 0, column= 0)
        self.nameContent = ttk.Label(self.projectFrame, text = '')
        self.nameLabel.grid(row = 1, column= 0)
        self.startDateLabel = ttk.Label(self.projectFrame,text = 'Start Date: ')
        self.startDateLabel.grid(row=2, column= 0)
        self.endDateLabel = ttk.Label(self.projectFrame,text = 'End Date: ')
        self.endDateLabel.grid(row=3, column= 0)
        self.descriptionLabel = ttk.Label(self.projectFrame, text = "Description: ")
        self.descriptionLabel.grid(row=4, column = 0)

        #Button to change the content
        self.nameChangeButton = ttk.Button(self.projectFrame, text = 'Change Name', command = self.clickChangeName)
        self.nameChangeButton.grid(row= 1, column= 1)
        self.startDateButton = ttk.Button(self.projectFrame, text = 'Change Date', command= self.clickStartDate)
        self.startDateButton.grid(row=2, column=1)
        self.endDateButton = ttk.Button(self.projectFrame, text = 'Change Date', command= self.clickEndDate)
        self.endDateButton.grid(row=3, column=1)

        #Textbox for description
        self.descriptionTextbox = ScrolledText(self.projectFrame, height = 30, width=30)
        self.descriptionTextbox.grid(row=5,columnspan=2)
        
        #For the Budget frame
        #Labels
        self.budgetNameLabel = ttk.Label(self.budgetFrame, text = "Project's Budget: ")
        self.budgetNameLabel.grid(row = 0, column= 0, columnspan = 2)
        self.potentialBudgetLabel = ttk.Label(self.budgetFrame, text = "Potential Budget: ")
        self.potentialBudgetLabel.grid(row =1, column=0)
        self.plannedBudgetLabel = ttk.Label(self.budgetFrame, text = "Planned Budget: ")
        self.plannedBudgetLabel.grid(row = 3, column= 0)
        self.currentBudgetLabel = ttk.Label(self.budgetFrame, text = "Current Budget: ")
        self.currentBudgetLabel.grid(row= 5, column = 0)

        #Values
        self.potentialBudgetValue = ttk.Label(self.budgetFrame, text ="")
        self.potentialBudgetValue.grid(row = 2, column = 0)
        self.plannedBudgetValue = ttk.Label(self.budgetFrame, text = "")
        self.plannedBudgetValue.grid(row = 4, column= 0)
        self.currentBudgetValue = ttk.Label(self.budgetFrame, text = "")
        self.currentBudgetValue.grid(row = 6, column = 0)

        #Button
        self.potentialBudgetButton = ttk.Button(self.budgetFrame, text= "Change Potential Budget", command= self.clickChangeBudget)
        self.potentialBudgetButton.grid(row = 1, column = 1)

        #For the members frame
        #label
        self.memberLabel = ttk.Label(self.memberFrame, text= "Members in this project")
        self.memberLabel.grid(row= 0, column = 0, columnspan= 2)
        
        #Member treeview
        columns = ('name', 'email')
        self.memberTree = ttk.Treeview(self.memberFrame, columns=columns, show='headings', height = 15)

        # define headings
        self.memberTree.heading('name', text='Name')
        self.memberTree.heading('email', text='Email')
        self.memberTree.grid(row=1, column=0, columnspan=2)

        # add a scrollbar
        self.treeScrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.memberTree.yview)
        self.memberTree.configure(yscroll=self.treeScrollbar.set)
        self.treeScrollbar.grid(row=1, column=2, sticky='ns')

        #Buttons
        self.addMemberButton = ttk.Button(self.memberFrame, text= "Add Member", command= self.clickAddMember)
        self.addMemberButton.grid(row = 2,column=0)
        self.removeMemberButton = ttk.Button(self.memberFrame, text= "Remove Member", command = self.clickRemoveMember)
        self.removeMemberButton.grid(row= 2, column= 1)


        #Button to commit the changes to the info
        self.projectCommitChange = ttk.Button(self.projectFrame, text = "Commit Description Changes", command= self.commitDescriptionChange)
        self.projectCommitChange.grid(row=6,column=0)

        #set the controller
        self.controller = None
    """
    change name
    add member
    remove member
    
    """
    def setController(self, controller):
        self.controller = controller
    
    def clickStartDate(self):
        if self.controller:
            self.controller.pickStartDate(self)

    def clickEndDate(self):
        if self.controller:
            self.controller.pickEndDate(self)

    def commitDescriptionChange(self):
        if self.controller:
            self.controller.commitDescriptionChange(self)

    def clickShowSelectedInfo(self, event):
        if self.controller:
            self.controller.showSelectedInfo()
    
    def clickChangeBudget(self):
        if self.controller:
            self.controller.changeBudget()

    def clickAddMember(self):
        if self.controller:
            self.controller.addMember()

    def clickRemoveMember(self):
        if self.controller:
            self.controller.removeMember()

    def clickChangeName(self):
        if self.controller:
            self.controller.changeName()

    def refreshSelfInfo(self):
        if self.controller:
            self.controller.refreshInfo()

class ProjectInfoWindowController:
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
        mycursor.execute("select `name`, `member_email` from `projectmember` pm INNER JOIN `users` u ON u.`email` = pm.`member_email` WHERE `project_name` = '{}';".format(self.app.project.getName()))
        memberList = mycursor.fetchall()
        self.app.project.setMemberList(memberList)
        for i in memberList:
            self.view.memberTree.insert('',tk.END,values=i)
        #self.view.memberTree.delete(*self.view.memberTree.get_children())
        """
        update the name
        get the start date and end date
        get the description
        get the budgets
        
        """
        self.view.nameLabel['text'] = self.app.project.getName()
        self.view.startDateButton['text'] = self.app.project.getStartDate()
        self.view.endDateButton['text'] = self.app.project.getEndDate()
        self.view.potentialBudgetValue['text'] = self.app.project.getPotentialBudget()
        mycursor.execute("SELECT SUM(`cost`) from `tasks` where `project_name` = '{}';".format(self.app.project.getName()))
        self.view.plannedBudgetValue['text'] = mycursor.fetchall()[0][0]
        self.view.descriptionTextbox.insert('1.0',self.app.project.getDescription())
        try:
            self.view.currentBudgetValue['text'] = int(self.app.project.getPotentialBudget()) - int(self.view.plannedBudgetValue['text'])
        except ValueError:
            self.view.plannedBudgetValue['text']=0
            self.view.currentBudgetValue['text'] = int(self.app.project.getPotentialBudget()) - int(self.view.plannedBudgetValue['text'])
        #For when the user is not the manager
        if self.app.user.getEmail() != self.app.project.getManagerEmail():
            self.view.nameChangeButton['state'] = 'disabled'
            self.view.startDateButton['state'] = 'disabled'
            self.view.endDateButton['state'] = 'disabled'
            self.view.potentialBudgetButton['state'] = 'disabled'
            self.view.descriptionTextbox['state'] = 'disabled'
            self.view.addMemberButton.grid_remove()
            self.view.removeMemberButton.grid_remove()


    def refreshInfo(self):
        self.mydb.reconnect(attempts=1, delay=0)
        mycursor = self.mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        mycursor.execute("select `name`, `member_email` from `projectmember` pm INNER JOIN `users` u ON u.`email` = pm.`member_email` WHERE `project_name` = '{}';".format(self.app.project.getName()))
        memberList = mycursor.fetchall()
        self.app.project.setMemberList(memberList)
        self.view.memberTree.delete(*self.view.memberTree.get_children())
        for i in memberList:
            self.view.memberTree.insert('',tk.END,values=i)
       
        """
        update the name
        get the start date and end date
        get the description
        get the budgets
        
        """
        self.view.nameLabel['text'] = self.app.project.getName()
        self.view.startDateButton['text'] = self.app.project.getStartDate()
        self.view.endDateButton['text'] = self.app.project.getEndDate()
        self.view.potentialBudgetValue['text'] = self.app.project.getPotentialBudget()
        mycursor.execute("SELECT SUM(`cost`) from `tasks` where `project_name` = '{}';".format(self.app.project.getName()))
        self.view.plannedBudgetValue['text'] = mycursor.fetchall()[0][0]
        self.view.descriptionTextbox.delete('1.0', tk.END)
        self.view.descriptionTextbox.insert('1.0',self.app.project.getDescription())
        try:
            self.view.currentBudgetValue['text'] = int(self.app.project.getPotentialBudget()) - int(self.view.plannedBudgetValue['text'])
        except ValueError:
            self.view.plannedBudgetValue['text']=0
            self.view.currentBudgetValue['text'] = int(self.app.project.getPotentialBudget()) - int(self.view.plannedBudgetValue['text'])

    def pickStartDate(self, view):
        root = tk.Toplevel()
 
        # Set geometry
        todayDate = self.app.project.getStartDate().strftime('%Y-%m-%d').split('-')
        # Add Calendar
        cal = Calendar(root, selectmode = 'day',
                    year = int(todayDate[0]), month = int(todayDate[1]),
                    day = int(todayDate[2]), date_pattern = 'yyyy-mm-dd')
        
        cal.grid(row = 0)
        
        def getDate():
            view.startDateButton['text']= cal.get_date()
            self.app.project.setStartDate(datetime.strptime(cal.get_date(),'%Y-%m-%d'))
            self.app.project.update()
            self.mydb.reconnect(attempts=1, delay=0)
            root.destroy()
        
        # Add Button and Label
        getSelectedDateButton = ttk.Button(root, text = "Get Date",command = getDate)
        getSelectedDateButton.grid(row =1)

    #literally a duplicate of the one above
    def pickEndDate(self, view):
        root = tk.Toplevel()
 
        # Set geometry
        todayDate = self.app.project.getEndDate().strftime('%Y-%m-%d').split('-')
        
        # Add Calendar
        cal = Calendar(root, selectmode = 'day',
                    year = int(todayDate[0]), month = int(todayDate[1]),
                    day = int(todayDate[2]), date_pattern = 'yyyy-mm-dd')
        
        cal.grid(row = 0)
        
        def getDate():
            view.endDateButton['text']= cal.get_date()
            self.app.project.setEndDate(datetime.strptime(cal.get_date(),'%Y-%m-%d'))
            self.app.project.update()
            self.mydb.reconnect(attempts=1, delay=0)
            root.destroy()
        
        # Add Button and Label
        getSelectedDateButton = ttk.Button(root, text = "Get Date",command = getDate)
        getSelectedDateButton.grid(row =1)

    def commitDescriptionChange(self, view):
        descriptionContent = view.descriptionTextbox.get('1.0', tk.END)
        self.app.project.setDescription(descriptionContent)
        self.app.project.update()
        self.refreshInfo()

    def changeBudget(self):
        changeBudgetWindow = tk.Toplevel()

        changeBudgetFrame = ttk.Frame(changeBudgetWindow)
        changeBudgetFrame.grid(row=0, column=0, padx=10, pady=10)
        #label
        changeBudgetLabel = ttk.Label(changeBudgetFrame, text = "Input the budget")
        changeBudgetLabel.grid(row = 0, column= 0)
        
        #Entry
        budget = tk.StringVar()
        budgetEntry = ttk.Entry(changeBudgetFrame, textvariable=budget, width = 40)
        budgetEntry.grid(row = 1, column= 0)
        
        def changeBudget():
            self.view.potentialBudgetValue['text'] = budget.get()
            self.app.project.setPotentialBudget(int(budget.get()))
            self.app.project.update()
            self.refreshInfo()
            changeBudgetWindow.destroy()

        #button
        confirmBudgetButton = ttk.Button(changeBudgetFrame, text= "Confirm change", command = changeBudget)
        confirmBudgetButton.grid(row= 2, column= 0)

    def addMember(self):
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
        mycursor.execute("SELECT `email` FROM `users` WHERE `email` NOT IN (select `member_email` from `projectmember` WHERE `project_name` = '{}');".format(self.app.project.getName()))
        memberList = mycursor.fetchall()
        if memberList == []:
            addMemberWindow.destroy()
            print("No more people to add")
            return
        memberVar.set(memberList)
        def Scankey(event):
            
            val = event.widget.get()
            

            if val == '':
                data = memberList
            else:
                data = []
                for item in memberList[0]:
                    if val.lower() in item.lower():
                        data.append(item)				

            
            update(data)


        def update(data):
            memberVar.set(data)

        def chooseMember(event):
            currentSelection = memberBox.curselection()
            toBeChecked = memberBox.get(currentSelection[0])
            mycursor = self.mydb.cursor()
            mycursor = self.mydb.cursor()
            mycursor.execute("USE InformationManagementSystem;")
            mycursor.execute("SELECT `email` FROM `users` WHERE `email` NOT IN (select `member_email` from `projectmember` WHERE `project_name` = '{}');".format(self.app.project.getName()))
            memberList = mycursor.fetchall()
            memberList.remove(toBeChecked)
            memberVar.set(memberList)
            mycursor.execute("USE InformationManagementSystem;")
            mycursor.execute("SELECT `name`, `email` FROM `users` WHERE `email` = '{}';".format(toBeChecked[0]))
            pMemberList = mycursor.fetchall()[0]
            self.app.project.getMemberList().append(pMemberList)
            self.app.project.update()
            self.refreshInfo()


        #Bind the search function
        searchEntry.bind('<KeyRelease>', Scankey)
        #bind double click action to listbox
        memberBox.bind('<Double-1>', chooseMember)

    def removeMember(self):
        currentItem = self.view.memberTree.focus()
        currentSelection = self.view.memberTree.item(currentItem)
        selectedValue = currentSelection['values']
        if selectedValue[1] != self.app.project.getManagerEmail():
            self.app.project.getMemberList().remove(tuple(selectedValue))
            mycursor = self.mydb.cursor()
            mycursor.execute("USE InformationManagementSystem;")
            mycursor.execute("DELETE FROM `ProjectMember` WHERE (`member_email` = '{}') and (`project_name` = '{}');".format(selectedValue[1], self.app.project.getName()))
            self.mydb.commit()
            self.refreshInfo()
        else:
            print("Can't remove manager")

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
                    self.app.project.updateName(newName)
                    self.refreshInfo()
                    changeNameWindow.destroy()
                except mysql.connector.IntegrityError:
                    showError("There's already a project with that name")


        #Name change button
        changeNameButton = ttk.Button(changeNameFrame, text="Change Name", command=changeName)
        changeNameButton.grid(row=1, column= 0, padx=5, pady=5)
        


class ProjectInfoWindowApp(tk.Tk):
    def __init__(self, user, project):
        super().__init__()
        self.user = user
        self.project = project
        self.title("Project Info")

        #create a view and place it on the root window
        view = ProjectInfoWindowView(self)
        view.grid(row = 0, column = 0, padx = 10, pady = 10)

        #create the project info controller
        controller = ProjectInfoWindowController(view,self)

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
    app = ProjectInfoWindowApp(loginUser,chosenProject)
    app.mainloop()

