from domains import Task, Project, User
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Ch0keYourselfT0Sle#p"
)
mycursor = mydb.cursor()
mycursor.execute("USE InformationManagementSystem;")
mycursor.execute("SELECT username, password FROM Users")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)