# Julian Fliegler
# CS 457, PA2
# Dec 2022

import os
import string
import sys

# custom exceptions
class Error(Exception):
    # Base class for other exceptions
    pass
class NoSemicolonExcept(Error):
    # if user input doesn't end in semicolon
    pass
class AbortExcept(Error):
    # if try to commit when don't have lock
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

# gets list of vars given delimiting string and lets you choose string to split on
def getVarBtwnStrs(inputStr, start, end, splitOn):
    return (inputStr.split(start))[1].split(end)[0].split(splitOn)

# gets var after some delimiting string (end)
def getInputAfterStr(inputStr, end):
    return inputStr[:-1].split(end)[1].split(" ")[0]

def getHeader(f):
    # get first line (header)
    content = f.readline() 
    # turn header into list to be able to index
    header = content.split("|") 
    return header

# performs inequalities for "where" statements
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

def getColIndex(table, attr):
    # get header
    with open(table, 'r') as file:
        header = file.readline().strip().split(" | ")
    
    # get index of attr 
    fullStr = [i for i in header if attr in i] # get full str ("id int") containing the attr ("id")
    index = header.index(fullStr[0]) # then find index of that str in header
    return index

# gets the list of indices that contain some selected cols
def findColIndices(f, header, cols):
    colIndex = []
    for i in range(len(header)):
        for j in range(len(cols)):
            if(header[i].find(cols[j]) != -1): # if is found
                colIndex.append(i)
    return colIndex

# for select
# concatenates all selected cols 
def appendSelectedCols(row, index, content):
    content += row[index] + " "
    return content

# matches a table name (Employee E) to desired attributes (E.id)
def match(tables, attrs):
    # parse attr list
    alias1 = attrs[0].split(".")[0]
    alias2 = attrs[1].split(".")[0]
    attr1 = attrs[0].split(".")[1]
    attr2 = attrs[1].split(".")[1]
    aliases = [alias1, alias2] 
    
    # create dictionary matching alias to attr
    dictAliasAttr = {alias1: attr1, alias2: attr2}

    # create dictionary matching alias to table name
    tables = " ".join(tables).split(" ") # reformat tables list
    dictAliasTable = {} # empty dict
    for a in aliases:
        if(a in tables):
            index = tables.index(a) - 1
            dictAliasTable[a] = tables[index]

    # perform match
    retTables = []
    retAttrs = []
    for i in range(len(dictAliasAttr)):
        retTables.append(dictAliasTable[aliases[i]])
        retAttrs.append(dictAliasAttr[aliases[i]])

    # return tables and their associated attrs
    return retTables, retAttrs

# performs inner join
def innerJoin(tables, indices, ineq):
    # reset vars
    joinedRows = ""
    header = ""

    with open(tables[0], 'r') as tableA:
        with open(tables[1], 'r') as tableB:
            # get headers
            header = (tableA.readline().strip() + " | " + tableB.readline().strip())

            # get rest of tables to read
            rowsTableA = tableA.readlines()
            rowsTableB = tableB.readlines()

            for rowA in rowsTableA:
                for rowB in rowsTableB:
                    # if match
                    if(whereHelper(rowA[indices[0]], rowB[indices[1]], ineq)):
                        joinedRows += (rowA.strip() + "|" + rowB.strip()) + '\n'

    newContent = (header + '\n' + joinedRows)
    return newContent

# performs LEFT outer join
def outerJoin(tables, indices, ineq):
    # reset vars
    joinedRows = ""
    header = ""

    with open(tables[0], 'r') as tableA:
        with open(tables[1], 'r') as tableB:
            # get headers
            header = (tableA.readline().strip() + " | " + tableB.readline().strip())

            # get rest of tables to read
            rowsTableA = tableA.readlines()
            rowsTableB = tableB.readlines()
            
            # if rowA match rowB, add row to joined table, matchCount++
            # if rowA doesn't match any rowB, add rowA to joined table
            for rowA in rowsTableA:
                matchCount = 0
                for rowB in rowsTableB:
                    if(whereHelper(rowA[indices[0]], rowB[indices[1]], ineq)):
                        joinedRows += (rowA.strip() + "|" + rowB.strip()) + '\n'
                        matchCount += 1
                if(matchCount == 0):
                    joinedRows += (rowA.strip() + "||") + '\n'

    newContent = (header + '\n' + joinedRows)
    return newContent

def performUpdate(file, recordCount):
    # get first line (header)
    newContent = file.readline()
    # turn header into list to be able to index
    header = newContent.split("|") 
    
    # get indices of "where" and "set" cols
    currIndex = 0;
    for attr in header:
        if attr.find(whereLeft) != -1: # if is found
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
        if(whereHelper(row[whereIndex], whereRight, whereIneq)):
            row[setIndex] = setVar 
            recordCount += 1
        # convert back to str
        row = "|".join(row) 
        # clean up 
        if(not row.endswith('\n')):
            row = row + '\n'
        # update content to be written
        newContent = newContent + row
    return newContent, recordCount


mode = 0o777 # give file permissions for mkdir
userInput = ""
tempInput = ""

# take user input until '.EXIT'
while(userInput != ".EXIT".casefold()):
    try:
        userInput = input().strip()

        if(userInput == ""): # ignore whitespace
            continue
        if(userInput.startswith("--")): # ignore file comments
            continue
        if(not userInput.endswith(";") and userInput != ".EXIT"): # read until ";"
            raise NoSemicolonExcept
        elif(userInput.endswith(";")):
            # concatenate all input since last ";" into single line
            tempInput = tempInput + " " + userInput
            userInput = tempInput
            tempInput = ""
            print("\n--" + userInput)
        
    except NoSemicolonExcept:
        # read input until user enters ";"
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
                tableName = getVarBtwnStrs(userInput, "TABLE ".casefold(), "(", ", ")[0].capitalize().strip()
                if(os.path.exists(tableName)):
                    raise FileExistsError

                # split string after table name
                # remove first, last parantheses and ";"
                # then replace all commas with "|"
                tableContent = userInput.split(tableName)[1] # content after table name
                tableContent = getVarBtwnStrs(tableContent, "(", ")", ", ") # content in between parantheses; str -> list
                tableContent = "|".join(tableContent) # list -> string, joined by "|"

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
                # empty strs
                newContent = ""
                newHeader = ""

                # vars to check which type of join
                inner = False
                outer = False
                where = False
                on = False
                
                # get data from user input
                if("WHERE".casefold() in userInput):
                    where = True
                    delimStr = " where ".casefold()
                    whereLeft = getInputAfterStr(userInput, " WHERE ".casefold())
                    whereIneq = getInputAfterStr(userInput, whereLeft + " ")
                    whereRight = getInputAfterStr(userInput, whereIneq + " ")
                    whereList = [whereLeft, whereRight, whereIneq]

                elif("on".casefold() in userInput):
                    on = True
                    delimStr = " on ".casefold()
                    onLeft = getInputAfterStr(userInput, " on ".casefold())
                    onIneq = getInputAfterStr(userInput, onLeft + " ")
                    onRight = getInputAfterStr(userInput, onIneq + " ")
                    onList = [onLeft, onRight, onIneq]

                cols = getVarBtwnStrs(userInput, 'SELECT '.casefold(), ' FROM '.casefold(), ", ")

                # get table names
                # parse will be diff based on join type
                if("inner join".casefold() in userInput):
                    inner = True
                    tableNames = getVarBtwnStrs(userInput, " FROM ".casefold(), delimStr, " inner join ".casefold())
                elif("outer join".casefold() in userInput):
                    outer = True
                    tableNames = getVarBtwnStrs(userInput, " FROM ".casefold(), delimStr, " left outer join ".casefold())
                elif("where".casefold() in userInput or "on".casefold() in userInput):
                    inner = True
                    tableNames = getVarBtwnStrs(userInput, " FROM ".casefold(), delimStr, ", ")
                else: # not a join statement, only one table
                    tableName = getInputAfterStr(userInput, " FROM ".casefold())

                with open(tableName, "r") as file: 
                    # top level conditions: check SELECT statement
                    # select all 
                    if("*" in cols): 
                        # secondary level: check FROM statement
                        if(not inner and not outer): # select * and not a join
                            # just print table contents 
                            print(bcolors.OKGREEN + file.read() + bcolors.ENDC)
                        elif(len(tableNames) < 0):
                            raise Exception("Cannot find table(s): " + tableNames) 

                        elif(len(tableNames) == 1): # select all from single table
                            # print entire table
                            print(bcolors.OKGREEN + file.read() + bcolors.ENDC)

                        else: # multiple tables given

                            if(inner and where): # inner join with WHERE clause
                                # match table names to attrs
                                tables = match(tableNames, whereList)[0]
                                attrs = match(tableNames, whereList)[1]

                                # get indices of each attr in each table
                                indices = []
                                for i in range(len(tables)):
                                    indices.append(getColIndex(tables[i], attrs[i]))
                                
                                # perform inner join
                                joinedTables = innerJoin(tables, indices, whereIneq)
                                print(bcolors.OKGREEN + joinedTables + bcolors.ENDC)

                            elif(inner and on): # inner join with ON clause
                                # match table names to attrs
                                tables = match(tableNames, onList)[0]
                                attrs = match(tableNames, onList)[1]

                                # get indices of each attr in each table
                                indices = []
                                for i in range(len(tables)):
                                    indices.append(getColIndex(tables[i], attrs[i]))
                                
                                # perform inner join
                                joinedTables = innerJoin(tables, indices, onIneq)
                                print(bcolors.OKGREEN + joinedTables + bcolors.ENDC)

                            elif(outer and on): # outer join and ON clause
                                # match table names to attrs
                                tables = match(tableNames, onList)[0]
                                attrs = match(tableNames, onList)[1]

                                # get indices of each attr in each table
                                indices = []
                                for i in range(len(tables)):
                                    indices.append(getColIndex(tables[i], attrs[i]))

                                # perform outer join
                                joinedTables = outerJoin(tables, indices, onIneq)
                                print(bcolors.OKGREEN + joinedTables + bcolors.ENDC)
                    # select specific cols
                    else:
                        # print only selected cols
                        header = getHeader(file)
                        indices = findColIndices(file, header, cols)

                        if("WHERE".casefold() in userInput):
                            whereLeft = whereLeft.split() # convert str to list to be compatible with findColIndices
                            whereIndex = findColIndices(file, header, whereLeft)[0] # will only work for one "where" argument

                        # only store header for selected cols
                        for j in range(len(indices)):
                            newHeader += header[indices[j]].strip() + "|" 
                        # clean up
                        newHeader = newHeader[:-1] + "\n"

                        # read rest of file
                        lines = file.readlines()
                        for row in lines:
                            row = row.split("|") # convert to list to use indices
                            for j in range(len(indices)):
                                # check each attr of each row meets "where" conds
                                if(whereHelper(row[whereIndex], whereRight, whereIneq)):
                                    newContent = appendSelectedCols(row, indices[j], newContent)
                            # clean up
                            newContent = newContent.strip().split(" ")
                            newContent = "|".join(newContent) + "\n" # convert back to string
                        print(bcolors.OKGREEN + newHeader + newContent + bcolors.ENDC)
                        
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
                colVals = userInput.split("(")[1][:-2].replace(",", "|").replace("'", "").replace("\t", "").replace(" ", "")

                # append to table
                with open(tableName, "a") as file:
                    file.write("\n")
                    file.write(colVals)
                print(bcolors.OKGREEN + "1 new record inserted." + bcolors.ENDC)
            except Exception as e:
                print("Error in insertion: ")
                print(e)

        elif("UPDATE" in userInput.upper()):
            try:
                # for success msg
                recordCount = 0
                
                # parse command
                # only works for singular args right now
                tableName = getInputVar(userInput, 1).capitalize()
                setCol = getInputVar(userInput, 3)
                setVar = getInputVar(userInput, 5).replace("'", "")
                whereLeft = getInputVar(userInput, 7)
                whereIneq = getInputVar(userInput, 8)
                whereRight = getInputVar(userInput, 9).replace("'", "")
            
                with open(tableName, 'r+') as file: # open for r+w
                    # check if transaction in progress
                    currDir = os.path.split(os.getcwd())[1] 
                    fileName = currDir + "_lock"
                    # if transaction not in progress peform update normally
                    if(not os.path.exists(fileName)): 
                            tempList = performUpdate(file, recordCount)
                            newContent = tempList[0]
                            recordCount = tempList[1]
                            rewriteFile(file, newContent)
                    else: # transaction in progress
                        # read file to check if pid matches curr process 
                        with open(fileName,"r") as f:
                            content = f.read()
                            if str(os.getpid()) in content: # if match
                                # curr process has lock
                                # store update but don't commit yet
                                with open("updates", "w") as f:
                                    # write table name so know which table to update later
                                    f.write(tableName + '\n')
                                    # write contents of update
                                    tempList = performUpdate(file, recordCount)
                                    f.write(tempList[0]) # write update to file
                                    recordCount = tempList[1]
                            else:
                                # curr process does not have lock
                                raise FileExistsError
                # success msgs
                if(recordCount == 1):
                    recsModified = "1 record"
                else:
                    recsModified = str(recordCount) + " records"
                print(bcolors.OKGREEN + recsModified + " modified." + bcolors.ENDC)
            except FileExistsError:
                print(bcolors.FAIL + "Error: Table " + tableName + " is locked!" + bcolors.ENDC)   

        elif("DELETE FROM" in userInput.upper()):
            try:
                # for success msg
                recordCount = 0

                # parse command
                tableName = getInputVar(userInput, 2).capitalize()
                whereLeft = getInputVar(userInput, 4)
                whereIneq = getInputVar(userInput, 5)
                whereRight = getInputVar(userInput, 6).replace("'", "")
                
                with open(tableName, 'r+') as file: # open for r+w
                    # get first line (header)
                    newContent = file.readline() 
                    # turn header into list to be able to index
                    header = newContent.split("|") 

                    # get indices of "where" col
                    currIndex = 0;
                    for attr in header:
                        if attr.find(whereLeft) != -1: # if is found
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
                        delete = (whereHelper(row[whereIndex], whereRight, whereIneq))
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
            except Exception as e:
                print("Error in delete: ")
                print(e)

        elif("BEGIN TRANSACTION" in userInput.upper()):
            try:
                # generate name of lock file
                currDir = os.path.split(os.getcwd())[1]
                fileName = currDir + "_lock"

                if(os.path.exists(fileName)): # if lock file already exists
                    pass # do nothing
                else: # create file
                    with open(fileName, "w") as f:
                        # write pid of current process
                        f.write(str(os.getpid()))
                
                print(bcolors.OKGREEN + "Transaction starts." + bcolors.ENDC) 
            except Exception as e:
                print("Error in begin transaction: ")
                print(e)

        elif("COMMIT" in userInput.upper()):
            try:
                # get lock file name
                fileName = os.path.split(os.getcwd())[1] + "_lock"

                # only commit if curr process has lock
                with open(fileName,"r") as f:
                    content = f.read()
                    if str(os.getpid()) in content: # curr process has lock
                        # perform updates and remove lock
                        with open("updates", 'r+') as file:
                            # first line is table name
                            tableName = file.readline().strip()
                            # rest of file is update to be made
                            lines = file.readlines() # read rest of file into new str
                            newContent = "";
                            for row in lines:
                                newContent += row.strip() + '\n'
                            # rewrite table with new str 
                            with open(tableName, 'r+') as updateFile:
                                rewriteFile(updateFile, newContent)
                        # del lock file and file containing now-commited updates
                        os.remove("updates")
                        os.remove(fileName)
                        print(bcolors.OKGREEN + "Transaction committed." + bcolors.ENDC) 
                    else: # curr process does not have lock
                        # not allowed to commit
                        raise AbortExcept
            except AbortExcept:
                print(bcolors.FAIL + "Transaction abort." + bcolors.ENDC)
else:
    print(bcolors.OKGREEN + "All done." + bcolors.ENDC)