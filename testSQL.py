import mysql.connector
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="Ch0keYourselfT0Sle#p"
)
mycursor = mydb.cursor()
mycursor.execute("USE InformationManagementSystem;")
mycursor.execute("INSERT IGNORE INTO `PROJECTMEM ;")
projectInfo = mycursor.fetchall()[0]
print(projectInfo)