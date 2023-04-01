from domains import Task, Project, User
import tkinter as tk
from tkinter import ttk
import mysql.connector
from RegisterWindowGUI import RegisterView,RegisterController,RegisterApp
from tkcalendar import Calendar
class ProjectAdderView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        #Create widgets
        #labels
        self.nameLabel = ttk.Label(self, text="Project name")
        self.nameLabel.grid(row= 0, column= 0)
        self.startDateLabel = ttk.Label(self, text= "Start Date")
        self.startDateLabel.grid(row = 3, column = 0)
        self.endDateLabel = ttk.Label(self, text= "End Date")
        self.endDateLabel.grid(row = 5, column= 0)
        self.potentialBudgetLabel = ttk.Label(self, text="Potential Budget")
        self.potentialBudgetLabel.grid(row = 7, column = 0)
        self.descriptionLabel = ttk.Label(self, text= "Description")
        self.descriptionLabel.grid(row = 9, column = 0)

        #Entry

    