# Julian Fliegler
# CS 457, PA1
# Oct 2022

import os
import sys

userInput = ""
tempInput = ""
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

def whereHelper(lt, rt, ieql):
    if(ieql == '='):
        return lt == rt
    elif(ieql == '!='):
        return lt != rt
    elif(ieql == '<'):
        return float(lt) < float(rt)
    elif(ieql == '>'):
        return float(lt) > float(rt)
    elif(ieql == '<='):
        return float(lt) <= float(rt)
    elif(ieql == '>='):
        return float(lt) >= float(rt)

def rewriteFile(f, content):
    # delete contents of file
    f.seek(0) # go to begin of file
    f.truncate()
    f.write(content)

def parseAttrs(inputStr, start, end):
    return (inputStr.casefold().split(start))[1].split(end)[0].split(", ")

def parseTable(inputStr, end):
    return inputStr[:-1].casefold().split(end)[1].split(" ")[0]

def findColIndices(f, cols):
    colIndex = []
    # get first line (header)
    newContent = f.readline() 
    # turn header into list to be able to index
    header = newContent.split("|") 
    # get indices of selected cols
    for i in range(len(header)):
        for j in range(len(cols)):
            if(header[i].find(cols[j]) != -1): # if is found
                colIndex.append(i)
    return colIndex


# take user input until '.EXIT'
while(userInput != ".EXIT"):
    try:
        userInput = input().strip()
        userInput = userInput.casefold()
       # print(userInput)

        if(userInput == ""):
            continue
        if(userInput.startswith("--")):
            continue
        if(not userInput.endswith(";") and userInput != ".EXIT"):
            raise NoSemicolonExcept
        elif(userInput.endswith(";")):
            tempInput = tempInput + " " + userInput
            userInput = tempInput
            tempInput = ""
            print("\n--" + userInput)
        
    except NoSemicolonExcept:
        tempInput = tempInput + " " + userInput
        continue
        #print(bcolors.FAIL + "Command must end in semicolon." + bcolors.ENDC)
    except EOFError:
        # when reach EOF
        sys.exit(0) # successful termination

    # if no exception
    else:
        if("CREATE DATABASE" in userInput.upper()):
            try:
                dbName = getInputVar(userInput, 2)
                os.mkdir(dbName, mode)
                print(bcolors.OKGREEN + "Database " + dbName + " created." + bcolors.ENDC)
            except FileExistsError:
                print(bcolors.FAIL + "!Failed to create database " + dbName + " because it already exists." + bcolors.ENDC)         

        elif("DROP DATABASE" in userInput.upper()):
            try:
                dbName = getInputVar(userInput, 2)
                os.rmdir(dbName)
                print(bcolors.OKGREEN + "Database " + dbName + " deleted." + bcolors.ENDC)
            except FileNotFoundError:
                print(bcolors.FAIL + "!Failed to delete " + dbName + " because it does not exist." + bcolors.ENDC)

        elif("USE" in userInput.upper()):
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

        elif("CREATE TABLE" in userInput.upper()):
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

        elif("DROP TABLE" in userInput.upper()):
            try:
                tableName = getInputVar(userInput, 2)
                os.remove(tableName)
                print(bcolors.OKGREEN + "Table " + tableName + " deleted." + bcolors.ENDC)
            except FileNotFoundError:
                print(bcolors.FAIL + "!Failed to delete " + tableName + " because it does not exist." + bcolors.ENDC)
        
        elif("SELECT".casefold() in userInput):
            try:
                start = 'SELECT '.casefold()
                end = ' FROM '.casefold()
                cols = parseAttrs(userInput, start, end)
                print(cols)
                tableName = parseTable(userInput, end)

                with open(tableName, "r") as file: 
                    if(cols == '*'):
                        print("*")
                    else:
                        indices = findColIndices(file, cols)
            

                    print(bcolors.OKGREEN + file.read() + bcolors.ENDC)
            except FileNotFoundError:
                print(bcolors.FAIL + "!Failed to query table " + tableName + " because it does not exist." + bcolors.ENDC)

        elif("ALTER TABLE" and "ADD" in userInput.upper()):
            try:
                tableName = getInputVar(userInput, 2)
                # after "ADD", take all characters except ";" 
                tableContent = " | " + userInput.split("ADD")[1][1:-1]
                with open(tableName, "a") as file: # append file
                    file.write(tableContent)
                print(bcolors.OKGREEN + "Table " + tableName + " modified." + bcolors.ENDC)
            except FileNotFoundError:
                print(bcolors.FAIL + "!Failed to modify " + tableName + " because it does not exist." + bcolors.ENDC)

        elif("INSERT INTO" in userInput.upper()):
            try:
                tableName = getInputVar(userInput, 2)
                # after "VALUES", take all characters except ";", get rid of commas and extra spaces
                colNames = userInput.split("values")[1][1:-2].replace(",", "|").replace("'", "").replace("\t", "").replace(" ", "")
                print(colNames)

                # get each individual attr
                # for x in colNames:
                #     x.strip()
                #     print(x)

                # append to table
                with open(tableName, "a") as file: # append file
                    file.write("\n")
                    file.write(colNames)
                print(bcolors.OKGREEN + "1 new record inserted." + bcolors.ENDC)
            except Exception as e:
                print("Error in insertion: ")
                print(e)

        elif("UPDATE" in userInput.upper()):
            try:
                # for success msg
                recordCount = 0

                # parse command
                tableName = getInputVar(userInput, 1)
                setCol = getInputVar(userInput, 3)
                setVar = getInputVar(userInput, 5).replace("'", "")
                whereCol = getInputVar(userInput, 7)
                ineqlity = getInputVar(userInput, 8)
                whereVar = getInputVar(userInput, 9).replace("'", "")
            
                with open(tableName, 'r+') as file: # open for r+w
                    # get first line (header)
                    newContent = file.readline() 
                    # turn header into list to be able to index
                    header = newContent.split("|") 
                    
                    # get indices of "where" and "set" cols
                    currIndex = 0;
                    for attr in header:
                        if attr.find(whereCol) != -1: # if is found
                            whereIndex = currIndex
                        if attr.find(setCol) != -1:
                            setIndex = currIndex
                        currIndex += 1

                    # read rest of file
                    lines = file.readlines()
                    # perform replacements ("set")
                    for row in lines:
                        # ignore whitespace
                        if(row == '\n'): 
                            continue
                        # convert to list to use indices
                        row = row.split("|") 
                        # perform replacement
                        if(whereHelper(row[whereIndex], whereVar, ineqlity)):
                            row[setIndex] = setVar 
                            recordCount += 1
                        # convert back to str
                        row = "|".join(row) 
                        # clean up 
                        if(not row.endswith('\n')):
                            row = row + '\n'
                        # update content to be written
                        newContent = newContent + row

                    rewriteFile(file, newContent)

                # success msgs
                if(recordCount == 1):
                    recsModified = "1 record"
                else:
                    recsModified = str(recordCount) + " records"
                print(bcolors.OKGREEN + recsModified + " modified." + bcolors.ENDC)
            except Exception as e:
                print("Error in update: ")
                print(e)


        elif("DELETE FROM" in userInput.upper()):
            # for success msg
            recordCount = 0

            # parse command
            tableName = getInputVar(userInput, 2).capitalize()
            whereCol = getInputVar(userInput, 4)
            ineqlity = getInputVar(userInput, 5)
            whereVar = getInputVar(userInput, 6).replace("'", "")
            

            with open(tableName, 'r+') as file: # open for r+w
                # get first line (header)
                newContent = file.readline() 
                # turn header into list to be able to index
                header = newContent.split("|") 

                # get indices of "where" col
                currIndex = 0;
                for attr in header:
                    if attr.find(whereCol) != -1: # if is found
                        whereIndex = currIndex
                    currIndex += 1

                # read rest of file
                lines = file.readlines()
                # perform deletions
                for row in lines:
                    # ignore whitespace
                    if(row == '\n'): 
                        continue
                    # convert to list to use indices
                    row = row.split("|") 
                    # determine if row to be deleted
                    delete = (whereHelper(row[whereIndex], whereVar, ineqlity))
                    # convert back to str
                    row = "|".join(row) 
                    # delete rows
                    if(delete):
                        row = ""
                        recordCount += 1
                    # clean up 
                    if(not row.endswith('\n')):
                        row = row + '\n'
                    # update content to be written
                    if(len(row) > 1):
                        newContent = newContent + row

                rewriteFile(file, newContent)

            # success msgs
            if(recordCount == 1):
                recsModified = "1 record"
            else:
                recsModified = str(recordCount) + " records"
            print(bcolors.OKGREEN + recsModified + " deleted." + bcolors.ENDC)

else:
    print(bcolors.OKGREEN + "All done." + bcolors.ENDC)