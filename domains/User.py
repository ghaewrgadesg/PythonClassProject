import mysql.connector
"""
overview: Users are the people who use the program
attributes:  
    name  String
    username String
    email String
    password String       
object: A typical Customer is c=<u,p,e,n>, where username(u), password(p), email(e), name(n).
abstract_properties:
    mutable(name)=true /\ optional(name)=false /\ length(name)=50
    mutable(username)=false /\ optional(username)=false /\ length(username)= 50
    mutable(password)=true /\ optional(password)=false /\ min_length(password) = 8 /\ max_length(password) = 254
    mutable(email)=true /\ optional(email)=false / max_length(email) = 254
author ghaewrgadesg 
 *"""
class User:
    #Constants for attributes
    NAME_LENGTH = 50
    USERNAME_LENGTH = 50
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 254
    MAX_EMAIL_LENGTH = 254

    def __init__(self,username, password, email, name):
        if len(username) < self.USERNAME_LENGTH:
            self.__username = username
        else:
            raise ValueError("Username must be under 50 characters")
        if len(password) >= self.MIN_PASSWORD_LENGTH and len(password) <= self.MAX_PASSWORD_LENGTH:
            self.__password = password
        else:
            print(len(password))
            raise ValueError("Password must be over 8 characters and under 254 characters")
        if len(email) < self.MAX_EMAIL_LENGTH:
            self.__email = email
        else:
            raise ValueError("Email must be under 254 characters")
        if len(name) < self.NAME_LENGTH:
            self.__name = name
        else:
            raise ValueError("Name must be under 50 characters")

    #Creating the setter
    def setName(self,name):
        if len(name) < self.NAME_LENGTH:
            self.__name = name
        else:
            raise ValueError("Name must be under 50 characters")
    
    def setPassword(self, password):
        if len(password) > self.MIN_PASSWORD_LENGTH and len(password) < self.MAX_PASSWORD_LENGTH:
            self.__password = password
        else:
            raise ValueError("Password must be over 8 characters and under 254 characters")

    def setEmail(self, email):
        if len(email) < self.MAX_EMAIL_LENGTH:
            self.__email = email
        else:
            raise ValueError("Email must be under 254 characters")
    
    #creating the getter
    def getName(self):
        return self.__name
    
    def getUsername(self):
        return self.__username
    
    def getPassword(self):
        return self.__password
    
    def getEmail(self):
        return self.__email
    
    def save(self):
        global databasePassword
        with open("databasePassword.txt") as f:
            databasePassword = f.readline().rstrip()
            print(databasePassword)
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=databasePassword
        )
        mycursor = mydb.cursor()
        mycursor.execute("USE InformationManagementSystem;")
        print("test")
        mycursor.execute("INSERT IGNORE INTO `Users` (`email`, `name`, `username`, `password`) VALUES ('{}', '{}', '{}', '{}');".format(self.__email, self.__name, self.__username, self.__password))
        #commit the changes to database
        mydb.commit()