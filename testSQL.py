import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Ch0keYourselfT0Sle#p"
)

mycursor = mydb.cursor()
mycursor.execute("USE InformationManagementSystem;")
mycursor.execute("INSERT IGNORE INTO `Users` (`email`, `name`, `username`, `password`) VALUES ('test', 'gamer', 'hamer', 'kromer');")
mycursor.execute("SELECT * FROM Users")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

mycursor.execute("SELECT * FROM Tasks")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
  