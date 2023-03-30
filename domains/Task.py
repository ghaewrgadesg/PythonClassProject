from datetime import date
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
    mutable(cost)=true /\ optional(cost)=false
    mutable(name)=true /\ optional(name)=false /\ length(username)= 100
    mutable(startDate)=true /\ optional(startDate)=false
    mutable(endDate)=true /\ optional(endDate)=false /
    mutable(status)=true /\ optional(status)=false /
author: Gnaff-and-my-Delusional-Kidneys
*"""
class Task:
    #Constants for attributes
    NAME_LENGTH = 100
    def __init__(self, name, startDate, endDate, status, description):
        if len(name) < self.NAME_LENGTH:
            self.__name = name
        else:
            raise ValueError("Task name must be under 100 characters")
        self.__startDate = startDate
        self.__endDate = endDate    
        self.__status = status
        self.__description = description
        self.__assignedMemberList = []
    
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