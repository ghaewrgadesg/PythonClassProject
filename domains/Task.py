"""
overview:
attributes:  
    cost: Int
    name: String
    start date: String 
    end date: String
    status: String
object:
abstract_properties:
author: Gnaff-and-my-Delusional-Kidneys
*"""
class Project:
    #Constants for attributes
    NAME_LENGTH = 100
    def __init__(self, name, start_date, end_date, status, description):
        if len(name) < self.NAME_LENGTH:
            self.__name = name
        else:
            raise ValueError("Task name must be under 100 characters")
        self.__start_date = start_date
        self.__end_date = end_date    
        self.__status = status
        self.__description = description
        self.__assigned_member_list = []
    #Creating the setter
    def set_name(self,name):
        if len(name) < self.NAME_LENGTH:
            self.__name = name
        else:
            raise ValueError("Task name must be under 100 characters")
    def set_start_date(self, start_date): self.__start_date = start_date   
    def set_end_date(self, end_date): self.__end_date = end_date
    def set_status(self, status): self.__status = status
    def set_description(self, description): self.__description = description
    #Creating the getter
    def get_name(self):return self.__name
    def get_start_date(self): return self.__start_date
    def get_status(self, status): return self.__status
    def get_end_date(self): return self.__end_date
    def get_description(self): return self.__description
    #Input number of assigned members for this task and their information
    def inoamfttati(self):
        while True:
            try:
                n = int(input('Input number of member assigned to this task'))
            except ValueError: 
                print('Please try again')
                continue
            else: break
        self.__assigned_member_list = [0]*n
        for i in range(self.__assigned_member_list): self.__assigned_member_list[i] = input("Input assigned member's email: ")
    def get_mem_list(self): return self.__assigned_member_list