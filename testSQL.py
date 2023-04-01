import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ch0keYourselfT0Sle#p"
)


mycursor = mydb.cursor()
mycursor.execute("USE InformationManagementSystem;")
mycursor.execute("Select `project_name` From `Users` Join `ProjectMember` where `Username` = 'bthung2003'")
projects= mycursor.fetchall()
print(projects)