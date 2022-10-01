import os
import sys

userInput = None
mode = 0o777

# define Python user-defined exceptions
class Error(Exception):
    # Base class for other exceptions
    pass
class NoSemicolonExcept(Error):
    # if user input doesn't end in semicolon
    pass

def formatString(str, index):
    # remove last character
    # then split string by spaces and take substring at index
    fixedStr = str[:-1].split()[index]
    return fixedStr

while(userInput != '.EXIT'):
    try:
        userInput = input().strip()
        if(not userInput.endswith(";")):
            raise NoSemicolonExcept
    except NoSemicolonExcept:
        print("Command must end in semicolon.")
    except EOFError:
        # when reach EOF
        sys.exit(0) # successful termination

    # if no exception
    else:
        if("CREATE DATABASE" in userInput):
            try:
                dbName = formatString(userInput, 2)
                os.mkdir(dbName, mode)
                print("Database " + dbName + " created.")
            except FileExistsError:
                print("!Failed to create database " + dbName + " because it already exists.")         

        elif("DROP DATABASE" in userInput):
            try:
                dbName = formatString(userInput, 2)
                os.rmdir(dbName)
                print("Database " + dbName + " deleted.")
            except FileNotFoundError:
                print("!Failed to delete " + dbName + " because it does not exist.")

        elif("USE" in userInput):
            try:     
                dbName = formatString(userInput, 1)
                os.chdir(dbName)
                print("Using database " + dbName + ".")
            except FileNotFoundError:
                # while current dir isn't user inputted db
                while(not os.getcwd().endswith(dbName)):
                    os.chdir("..")
                    os.chdir(dbName)
                    print("Using database " + dbName + ".")
                else:
                    print("!Failed to use database " + dbName + " because it does not exist")

        elif("CREATE TABLE" in userInput):
            try:
                tableName = formatString(userInput, 2)
                if(os.path.exists(tableName)):
                    raise FileExistsError

                # split string after table name
                # take string from second character to all but last two chars
                # in other words, remove first and last parantheses and ";"
                # then replace all commas with "|"
                tableContent = userInput.split(tableName)[1][2:-2].replace(",", " |")
               
                with open(tableName, "w") as f: # "with" automatically closes file
                    f.write(tableContent)
                print("Table " + tableName + " created.")
            except FileExistsError:
                print("!Failed to create table " + tableName + " because it already exists.")

        elif("DROP TABLE" in userInput):
            try:
                tableName = formatString(userInput, 2)
                os.remove(tableName)
                print("Table " + tableName + " deleted.")
            except FileNotFoundError:
                print("!Failed to delete " + tableName + " because it does not exist.")
        
        elif("SELECT * FROM" in userInput):
            try:
                tableName = formatString(userInput, 3)
                with open(tableName, "r") as f: 
                    print(f.read())
            except FileNotFoundError:
                print("!Failed to query table " + tableName + " because it does not exist.")

        elif("ALTER TABLE" and "ADD" in userInput):
            try:
                tableName = formatString(userInput, 2)
                tableContent = " | " + userInput.split("ADD")[1][1:-1] # after add, take all characters except ";" 
                with open(tableName, "a") as file: # append file
                    file.write(tableContent)
                print("Table " + tableName + " modified.")
            except FileNotFoundError:
                print("!Failed to modify " + tableName + " because it does not exist.")
else:
    print("All done.")