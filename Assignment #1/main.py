import os
import re
import sys

userInput = None
mode = 0o777
# currDir = 
# start in Directory folder, create folder for each db and change to currDir 


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


#userInput = " "
#userInput = input()
while(userInput != '.EXIT'):
    try:
        userInput = input()
        if(not userInput.endswith(";")):
            raise NoSemicolonExcept
        # else:
        #     userInput = userInput.partition(";")[0]
        #print(userInput)
        #userInput = userInput.split(";")
        #print(userInput)
        
    except NoSemicolonExcept:
        print("Command must end in semicolon.")
    except EOFError:
        #print("Reached end of file")
        sys.exit(1)


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
            dbName = formatString(userInput, 1)
            os.chdir(dbName)
            print("Using database " + dbName + ".")
            #print(os.getcwd())

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
                #print(tableContent)
                f = open(tableName, "w") # overwrite mode, won't matter bc can't dupl files
                f.write(tableContent)
                f.close()
                print("Table " + tableName + " created.")

            except FileExistsError:
                print("!Failed to create table " + tableName + " because it already exists.")


        elif("DROP TABLE" in userInput):
            try:
                tableName = formatString(userInput, 2)
                os.remove(tableName)
            except FileNotFoundError:
                print("!Failed to delete " + tableName + " because it does not exist.")
        

        elif("SELECT * FROM" in userInput):
            try:
                tableName = formatString(userInput, 3)
                with open(tableName, "r") as f: # "with" automatically closes file
                    print(f.read())
            except FileNotFoundError:
                print("!Failed to query table " + tableName + " because it does not exist.")


        elif("ALTER TABLE" and "ADD" in userInput):
            try:
                tableName = formatString(userInput, 2)
                tableContent = " | " + userInput.split("ADD")[1][1:-1]
                with open(tableName, "a") as file: # append file
                    file.write(tableContent)
                print("Table " + tableName + " modified.")
            except FileNotFoundError:
                print("!Failed to modify " + tableName + " because it does not exist.")
else:
    print("All done.")           

# CREATE DATABASE db_1;
# CREATE DATABASE db_1;
# CREATE DATABASE db_2;
# DROP DATABASE db_2;
# DROP DATABASE db_2;
# CREATE DATABASE db_2;
# USE db_1;
# CREATE TABLE tbl_1 (a1 int, a2 varchar(20));
# CREATE TABLE tbl_1 (a3 float, a4 char(20));
# DROP TABLE tbl_1;
# DROP TABLE tbl_1;
# CREATE TABLE tbl_1 (a1 int, a2 varchar(20));
# SELECT * FROM tbl_1;
# ALTER TABLE tbl_1 ADD a3 float;
# SELECT * FROM tbl_1;
# CREATE TABLE tbl_2 (a3 float, a4 char(20));
# SELECT * FROM tbl_2;
# USE db_2;
# SELECT * FROM tbl_1;
# CREATE TABLE tbl_1 (a3 float, a4 char(20));
# SELECT * FROM tbl_1;
 