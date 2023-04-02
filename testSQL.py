import mysql.connector
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="Ch0keYourselfT0Sle#p"
)
mycursor = mydb.cursor()
mycursor.execute("USE InformationManagementSystem;")
mycursor.execute("SELECT `name`, `start_date`, `end_date` FROM `informationmanagementsystem`.`Project` WHERE (`name` = 'Sacrifice them all');")
projectInfo = mycursor.fetchall()[0]
print(projectInfo)