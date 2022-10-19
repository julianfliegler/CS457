# Julian Fliegler
# CS 457, PA1
# Oct 2022

import os
import sys

userInput = None
mode = 0o777 # give file permissions for mkdir

# custom exceptions
class Error(Exception):
    # Base class for other exceptions
    pass
class NoSemicolonExcept(Error):
    # if user input doesn't end in semicolon
    pass

# python class to print colored output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# gets variable from user input at index
def getInputVar(str, index):
    # remove last character
    # then split string by spaces and take substring at index
    inputVar = str[:-1].split()[index]
    return inputVar

# take user input until '.EXIT'
while(userInput != ".EXIT"):
    try:
        userInput = input().strip()

        if(userInput == ""):
            continue
        if(userInput.startswith("--")):
            continue
        if(not userInput.endswith(";") and userInput != ".EXIT"):
            raise NoSemicolonExcept

        print("\n-- " + userInput)
        
    except NoSemicolonExcept:
        print(bcolors.FAIL + "Command must end in semicolon." + bcolors.ENDC)
    except EOFError:
        # when reach EOF
        sys.exit(0) # successful termination

    # if no exception
    else:
        if("CREATE DATABASE" in userInput):
            try:
                dbName = getInputVar(userInput, 2)
                os.mkdir(dbName, mode)
                print(bcolors.OKGREEN + "Database " + dbName + " created." + bcolors.ENDC)
            except FileExistsError:
                print(bcolors.FAIL + "!Failed to create database " + dbName + " because it already exists." + bcolors.ENDC)         

        elif("DROP DATABASE" in userInput):
            try:
                dbName = getInputVar(userInput, 2)
                os.rmdir(dbName)
                print(bcolors.OKGREEN + "Database " + dbName + " deleted." + bcolors.ENDC)
            except FileNotFoundError:
                print(bcolors.FAIL + "!Failed to delete " + dbName + " because it does not exist." + bcolors.ENDC)

        elif("USE" in userInput):
            try:     
                dbName = getInputVar(userInput, 1)
                os.chdir(dbName)
                print(bcolors.OKGREEN + "Using database " + dbName + "." + bcolors.ENDC)
            except FileNotFoundError:
                # if current dir isn't user inputted db, go to root folder
                while(not os.getcwd().endswith("pa1")):
                    os.chdir("..")
                # if user inputted db exists, go to that db
                if(os.path.isdir(dbName)):                
                    os.chdir(dbName)
                    print(bcolors.OKGREEN + "Using database " + dbName + "." + bcolors.ENDC)
                else:
                    print(bcolors.FAIL + "!Failed to use database " + dbName + " because it does not exist" + bcolors.ENDC)

        elif("CREATE TABLE" in userInput):
            try:
                tableName = getInputVar(userInput, 2)
                if(os.path.exists(tableName)):
                    raise FileExistsError

                # split string after table name
                # remove first, last parantheses and ";"
                # then replace all commas with "|"
                tableContent = userInput.split(tableName)[1][2:-2].replace(",", " |")
               
                with open(tableName, "w") as f: # "with" automatically closes file
                    f.write(tableContent)
                print(bcolors.OKGREEN + "Table " + tableName + " created." + bcolors.ENDC)
            except FileExistsError:
                print(bcolors.FAIL + "!Failed to create table " + tableName + " because it already exists." + bcolors.ENDC)

        elif("DROP TABLE" in userInput):
            try:
                tableName = getInputVar(userInput, 2)
                os.remove(tableName)
                print(bcolors.OKGREEN + "Table " + tableName + " deleted." + bcolors.ENDC)
            except FileNotFoundError:
                print(bcolors.FAIL + "!Failed to delete " + tableName + " because it does not exist." + bcolors.ENDC)
        
        elif("SELECT * FROM" in userInput):
            try:
                tableName = getInputVar(userInput, 3)
                with open(tableName, "r") as f: 
                    print(bcolors.OKGREEN + f.read() + bcolors.ENDC)
            except FileNotFoundError:
                print(bcolors.FAIL + "!Failed to query table " + tableName + " because it does not exist." + bcolors.ENDC)

        elif("ALTER TABLE" and "ADD" in userInput):
            try:
                tableName = getInputVar(userInput, 2)
                # after "ADD", take all characters except ";" 
                tableContent = " | " + userInput.split("ADD")[1][1:-1]
                with open(tableName, "a") as file: # append file
                    file.write(tableContent)
                print(bcolors.OKGREEN + "Table " + tableName + " modified." + bcolors.ENDC)
            except FileNotFoundError:
                print(bcolors.FAIL + "!Failed to modify " + tableName + " because it does not exist." + bcolors.ENDC)

        elif("insert into" in userInput):
            try:
                tableName = getInputVar(userInput, 2)
                print(tableName)
                # after "VALUES", take all characters except ";" 
                # get rid of commas
                colNames = userInput.split("values")[1][1:-2].replace(",", "").replace("'", "").split("\t")
                #print(colNames)
                for x in colNames:
                    x.strip()
                    print(x)
                    # create list
                    (x) = []
                # with open(tableName, "a") as file: # append file
                #     file.write(tableContent)
                # print(bcolors.OKGREEN + "1 new record inserted." + bcolors.ENDC)
            except:
                print("Error in insertion")
else:
    print(bcolors.OKGREEN + "All done." + bcolors.ENDC)