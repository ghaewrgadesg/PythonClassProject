from datetime import date
import mysql.connector
"""
overview:
attributes:  
    cost: Int
    name: String
    startDate: date 
    endDate: date
    status: String
object:
abstract_properties:
    mutable(cost)=true /\ optional(cost)=false /\ min(cost) = 1
    mutable(name)=true /\ optional(name)=false /\ length(username)= 100
    mutable(startDate)=true /\ optional(startDate)=false
    mutable(endDate)=true /\ optional(endDate)=false /
    mutable(status)=true /\ optional(status)=false /
author: Gnaff-and-my-Delusional-Kidneys
*"""
class Task:
    #Constants for attributes
    NAME_LENGTH = 100
    MIN_COST = 1
    def __init__(self, name, startDate, endDate, status, description, cost):
        if len(name) < self.NAME_LENGTH:
            self.__name = name
        else:
            raise ValueError("Task name must be under 100 characters")
        self.__startDate = startDate
        self.__endDate = endDate    
        self.__status = status
        self.__description = description
        self.__assignedMemberList = []
        if cost > self.MIN_COST:
            self.__cost = cost
        else:
            raise ValueError("cost must be higher than 1")
    
    #Creating the setter
    def setName(self,name):
        if len(name) < self.NAME_LENGTH:
            self.__name = name
        else:
            raise ValueError("Task name must be under 100 characters")
    
    def setStartDate(self, startDate):
        self.__startDate = startDate   
   
    def setEndDate(self, endDate): 
        self.__endDate = endDate
   
    def setStatus(self, status): 
        self.__status = status
   
    def setDescription(self, description): 
        self.__description = description
   
    def setAssignedMember(self, members):
        self.__assignedMemberList = members

    #Creating the getter
    def get_name(self):
        return self.__name
   
    def get_startDate(self):
        return self.__startDate
   
    def get_status(self, status): 
        return self.__status
   
    def get_endDate(self):
        return self.__endDate
   
    def get_description(self):
        return self.__description
    
    def get_mem_list(self):
        return self.__assignedMemberList
    
    #saving the task to the database
    def save(self, projectName):
        """
        save the data of this task into the database
        :return:
        """
        global databasePassword
        with open("databasePassword.txt") as f:
            databasePassword = f.readline().rstrip()
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=databasePassword
        )
        mycursor = mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        print("test")
        """ 
        cost: Int
        name: String
        startDate: date 
        endDate: date
        status: String
        """
        mycursor.execute("INSERT IGNORE INTO `Tasks` (`name`, `start_date`, `end_date`, `description`, `cost`, `project_name`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(self.__name,  self.__startDate, self.__endDate, self.__description, self.__cost, projectName))
        #commit the changes to database

        mydb.commit()