import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import tkcalendar
from PIL import ImageTk, Image
from tkcalendar import Calendar, DateEntry
import datetime

root = tk.Tk()

myImg = ImageTk.PhotoImage(Image.open("banner.png"))
bannerLabel = ttk.Label(root, image = myImg)
bannerLabel.grid(row = 0, columnspan = 2)

root.mainloop()