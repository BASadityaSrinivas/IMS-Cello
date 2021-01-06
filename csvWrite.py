import csv
import os.path
from os import path

def createJumboColor(fileName):
    filePath = "csvFiles/" + fileName
    with open(filePath, 'w', newline='') as entryFile:
        writer = csv.writer(entryFile)
        writer.writerow(('Date','Color - White','New','Used'))
        entryFile.close()

# createJumboColor("jumboWhite.csv")


def appendJumbo(param):
    filePath = ''

    col = param[4]
    if col=="White":
        filePath = "csvFiles/" + 'jumboWhite.csv'
    elif col=="Brown":
        filePath = "csvFiles/" + 'jumboBrown.csv'
    elif col=="Other":
        filePath = "csvFiles/" + 'jumboOther.csv'

    if filePath=='':
        return "File not found"

    if path.isfile(filePath)==False:
        createJumboColor(filePath[9:])

    with open(filePath, 'a+', newline='') as entryWriteFile:
        writer = csv.writer(entryWriteFile)
        writer.writerow((param[0],param[1],param[2],param[3]))
        entryWriteFile.close()

# param = ('2020-11-24','Add White','5','')
# appendJumboWhite(param)


def createEntry():
    with open('csvFiles/entry.csv', 'w',newline='') as entryFile:
        writer = csv.writer(entryFile)
        writer.writerow(('SNo','Date','Description','Made','Used Jumbos'))
        entryFile.close()
# createEntry()


def appendEntry(param):
    if path.isfile("csvFiles/entry.csv")==False:
        createEntry()

    with open('csvFiles/entry.csv', 'a+', newline='') as entryWriteFile:
        writer = csv.writer(entryWriteFile)
        writer.writerow(('',param[0],param[1],param[2],param[3]))
        entryWriteFile.close()

# param = ('', 'Brown Jumbo', '', 0)
# appendEntry(param)


def createProcessed(fileName, col):
    filePath = "csvFiles/ProcessedTapes/" + col + '/' + fileName
    with open(filePath, 'w', newline='') as entryFile:
        writer = csv.writer(entryFile)
        writer.writerow(('Date', 'Description', 'Made', 'Sold'))
        entryFile.close()


def appendProcessed(param):
    # paramProcess = (date,desc,made_qua,sold_qua,color,width,length)
    fileName = param[6][:-2] + '_' + param[5][:-2] +'.csv'
    if param[5][:-2]=='1/2':
        fileName = param[6][:-2] + '_' + '0.5' +'.csv'

    col = param[4]
    if col=="White":
        filePath = "csvFiles/ProcessedTapes/White/" + fileName
    elif col=="Brown":
        filePath = "csvFiles/ProcessedTapes/Brown/" + fileName
    elif col=="Other":
        filePath = "csvFiles/ProcessedTapes/Other/" + fileName

    if path.isfile(filePath)==False:
        createProcessed(fileName, col)

    with open(filePath, 'a+', newline='') as entryWriteFile:
        writer = csv.writer(entryWriteFile)
        writer.writerow((param[0],param[1],param[2],param[3]))
        entryWriteFile.close()

# param = ('2020-11-24', 'Created', '4', '', 'White', '1/2 \"', '30 m')
# appendProcessed(param)

def createOrder():
    with open('csvFiles/order.csv', 'w',newline='') as entryFile:
        writer = csv.writer(entryFile)
        writer.writerow(('SNo','Date','Customer name','Status','Order Details'))
        entryFile.close()


def orderExit(param):
    # param = (date, cName, status, orderDetails)
    if path.isfile("csvFiles/order.csv")==False:
        createOrder()

    n = 0
    with open('csvFiles/order.csv', newline='') as entryReadFile:
        reader = csv.DictReader(entryReadFile)
        for row in reader:
            if row['SNo'] != '':
                n = row['SNo']
        entryReadFile.close()

    with open('csvFiles/order.csv', 'a+', newline='') as entryWriteFile:
        writer = csv.writer(entryWriteFile)
        writer.writerow((int(n)+1,param[0],param[1],param[2],param[3]))
        entryWriteFile.close()
