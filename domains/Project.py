"""
overview:
attributes:  
    name: String
    manager: email String
    start date: String 
    end date: String
author: Gnaff-and-my-Delusional-Kidneys
*"""
class Project:
    #Constants for attributes
    NAME_LENGTH = 200
    def __init__(self, name, manager_email, start_date, end_date, description_string):
        if len(name) < self.NAME_LENGTH:
            self.__name = name
        else:
            raise ValueError("Project name must be under 200 characters")
        self.__manager_email = manager_email
        self.__start_date = start_date
        self.__end_date = end_date
        self.__description_string = description_string
        self.budget = self.Budget()
        self.member_list = []
    #Creating the setter
    def set_name(self,name):
        if len(name) < self.NAME_LENGTH:
            self.__name = name
        else:
            raise ValueError("Project name must be under 200 characters")
    def set_manager_email(self, manager_email): self.__manager_email = manager_email
    def set_start_date(self, start_date): self.__start_date = start_date   
    def set_end_date(self, end_date): self.__end_date = end_date
    def set_description_string(self, description_string): self.__description_string = description_string
    #Creating the getter
    def get_name(self):return self.__name
    def get_manager_email(self): return self.__manager_email
    def get_start_date(self): return self.__start_date
    def get_end_date(self): return self.__end_date
    def get_description_string(self): return self.__description_string
    #inner class
    class Budget:
        def __init__(self, potential_budget, planned_budget):
            self.__potential_budget = potential_budget
            self.__planned_budget = planned_budget
        def set_potential_budget(self,potential_budget): self.__potential_budget = potential_budget
        def set_planned_budget(self,planned_budget): self.__planned_budget = planned_budget
        def get_potential_budget(self): return self.__potential_budget
        def get_planned_budget(self): return self.__planned_budget
    def inomotp(self):
        n = int(input('Input number of student'))
        self.member_list = [0]*n
        for i in range(self.member_list): self.member_list[i] = input("Input project memeber's email: ")

