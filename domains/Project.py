from datetime import date
"""
overview:
attributes:  
    name: String
    managerEmail String
    startDate: date 
    endDate: date
    potentialBudget: int
    plannedBudget: int
    description: String
object:
abstract_properties:
    mutable(name)=true /\ optional(name)=false /\ length(name)=50
    mutable(managerEmail)=true /\ optional(managerEmail)=false
    mutable(startDate)=true /\ optional(startDate)=false
    mutable(endDate)=true /\ optional(endDate)=false /
    mutable(potentialBudget)=true /\ optional(potentialBudget)=false / min(potentialBudget) = 1
    mutable(plannedBudget)=true /\ optional(plannedBudget)=false / min(plannedBudget) = 1
    mutable(description)=true /\ optional(description)=true /
author: Gnaff-and-my-Delusional-Kidneys
*"""
class Project:
    #Constants for attributes
    NAME_LENGTH = 200
    MIN_BUDGET = 1
    
    def __init__(self, name, managerEmail, startDate, endDate, potentialBudget, plannedBudget, description):
        if len(name) < self.NAME_LENGTH:
            self.__name = name
        else:
            raise ValueError("Project name must be under 200 characters")
        self.__managerEmail = managerEmail
        self.__startDate = startDate
        self.__endDate = endDate
        self.__description = description
        if potentialBudget < self.MIN_BUDGET:
            self.__potentialBudget = potentialBudget
        else:
            raise ValueError("Budget must be higher than 1")
        if plannedBudget < self.MIN_BUDGET:
            self.__plannedBudget = plannedBudget
        else:
            raise ValueError("Budget must be higher than 1")
        self.__memberList = []
    
    #Creating the setter
    def setName(self,name):
        if len(name) < self.NAME_LENGTH:
            self.__name = name
        else:
            raise ValueError("Project name must be under 200 characters")
        
    def setManagerEmail(self, managerEmail): 
        self.__managerEmail = managerEmail

    def setStartDate(self, startDate): 
        self.__startDate = startDate   

    def setEndDate(self, endDate): 
        self.__endDate = endDate

    def setDescription(self, description): 
        self.__description = description

    def setMemberList(self, members):
        self.__memberList = members

    #Creating the getter
    def getName(self):
        return self.__name

    def getManagerEmail(self): 
        return self.__managerEmail

    def getStartDate(self): 
        return self.__startDate

    def getEndDate(self): 
        return self.__endDate

    def getDescription(self):
        return self.__description

    def getMemberList(self):
        return self.__memberList

    def set_potentialBudget(self,potentialBudget): 
        if potentialBudget < self.MIN_BUDGET:
            self.__potentialBudget = potentialBudget
        else:
            raise ValueError("Budget must be higher than 1")

    def set_plannedBudget(self,plannedBudget): 
        if plannedBudget < self.MIN_BUDGET:
            self.__plannedBudget = plannedBudget
        else:
            raise ValueError("Budget must be higher than 1")

    def get_potentialBudget(self): 
        return self.__potentialBudget
    
    def get_plannedBudget(self): 
        return self.__plannedBudget