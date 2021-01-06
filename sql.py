import sqlite3, json, ast, datetime, psycopg2, mysql.connector
from csvWrite import *

# Godaddy connection
# conn = LocalDB()

# cPanel SSH Password = #cPanel123
# database password = affxix
##########################################################################################################

# def goDaddyDB():
#     conn = mysql.connector.connect(host="148.66.138.143",database="i7333420_wp1",user="affixDashboard",password="affix",port="3306")
#     return conn

def LocalDB():
    conn = sqlite3.connect('db.sqlite3')
    return conn

def template():
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)

        sqlSelectQuery = """SELECT quantityInStock FROM celloApp_cellotypes WHERE color = ?"""
        cursor.execute(sqlSelectQuery, ('White',),)
        conn.commit()
        print("SQL Query Selected")
        cursor.close()

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")
# template()


def RawEdit(func, col, no):
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)
        selectQ = """SELECT quantityInStock FROM celloApp_cellotypes WHERE color = ?;"""
        cursor.execute(selectQ,(col,),)
        dummy = cursor.fetchone()
        present = dummy[0]

        if(func == 'add'):
            new = present + int(no)
        elif(func == 'sub'):
            new = present - int(no)

        if new >= 0:
            updateQuery = """UPDATE celloApp_cellotypes SET quantityInStock = ? WHERE color = ? """
            param = (new, col)
            cursor.execute(updateQuery, param)
            strP = func + " the " + col + " by " + str(no)
            # print(strP)
            print('\nRaw Material Updated')

        sqlSelectQuery = """SELECT * FROM celloApp_cellotypes"""
        # cursor.execute(sqlSelectQuery)
        # print(cursor.fetchall())
        conn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")

# RawEdit('add', 'White', 5)
# RawEdit('sub', 'White', 5)


def ProcessAdd(param):
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)

        sqlSelectQuery = """SELECT * FROM celloApp_processed """
        paramExists = param[:3]
        add_qua = param[3]
        sqlExixtsQuery = """SELECT id, quantity FROM celloApp_processed WHERE LENGTH=? AND WIDTH=? AND COLOR=?;"""
        cursor.execute(sqlExixtsQuery,paramExists)

        if(cursor.fetchone()!=None):
            cursor.execute(sqlExixtsQuery,paramExists)
            id = cursor.fetchone()[0]
            cursor.execute(sqlExixtsQuery,paramExists)
            old_qua = cursor.fetchone()[1]
            new_qua = old_qua + int(add_qua)
            sqlUpdateQuery = """UPDATE celloApp_processed SET quantity=? WHERE id=?;"""
            cursor.execute(sqlUpdateQuery,(new_qua, id,))
            strP = param[2] + " with "+ param[0] +" and " + param[1] + " Updated : +" + str(param[3])
            # print(strP)
            print("\nProcessed Updated")
        else:
            sqlInsertQuery = """INSERT INTO celloApp_processed (length, width, color, quantity, date) VALUES (?,?,?,?,?)"""
            cursor.execute(sqlInsertQuery, param)
            strP = param[2] + " with "+ param[0] +" and " + param[1] + " Added : " + str(param[3])
            # print(strP)
            print("\nProcessed Added")

        conn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")

# param = ('30 m', '1/2 \"', 'White', 5, '2020-11-24')
# ProcessAdd(param)


def processUsedJumbo(col, usedJumbo):
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)

        if(usedJumbo>0):
            updateQuery = """UPDATE celloApp_cellotypes SET quantityInStock = ? WHERE color = ? """
            selectQ = """SELECT quantityInStock FROM celloApp_cellotypes WHERE color = ?;"""
            cursor.execute(selectQ,(col,),)
            dummy = cursor.fetchone()
            present = dummy[0]
            new_Jumbo = present - usedJumbo
            if new_Jumbo >= 0:
                cursor.execute(updateQuery, (new_Jumbo, col,),)
                strP = col + " Jumbo decreased by -" + str(usedJumbo)
                # print(strP)
                print("\nRaw Material Updated by Processed")
            else:
                print("\nRaw material insufficient")

            conn.commit()
            cursor.close()

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")

# processUsedJumbo('Brown', 1)


def ProcessDel(param):
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)

        sqlDeleteQuery = """DELETE FROM celloApp_processed WHERE LENGTH=? AND WIDTH=? AND COLOR=?;"""
        cursor.execute(sqlDeleteQuery, param)
        conn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")


def OrderAdd(param):
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)

        orderString = str(param[4])
        param1 = (param[0], param[1], param[2], param[3], orderString)
        param = param1
        # print(param)
        # orderDict = ast.literal_eval(orderString) # Converting String to Dictionary
        sqlInsertQuery = """INSERT INTO celloApp_ordertable (oID, cName, status, payment, date, orderDetails) VALUES (?,?,?,?,?,?)"""

        pkQuery = """SELECT OId FROM celloApp_ordertable ORDER BY oID"""
        cursor.execute(pkQuery)
        oldPkArr = cursor.fetchall()
        # print(oldPkArr)

        if oldPkArr==[]:
            oldPk = 0
        else:
            oldPk = oldPkArr[-1][0]

        param = (oldPk+1,) + param
        cursor.execute(sqlInsertQuery, param)

        sqlSelectQuery = """SELECT * FROM celloApp_ordertable"""
        # cursor.execute(sqlSelectQuery)
        # print(cursor.fetchall())
        conn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")


def PaymentUpdate(param):
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)

        sqlSelectQuery = """SELECT * FROM celloApp_ordertable"""
        sqlUpdateQuery = """UPDATE celloApp_ordertable SET payment = ? WHERE oID = ?"""
        cursor.execute(sqlUpdateQuery, (param[1], param[0],),)
        conn.commit()
        cursor.close()
        return "Payment Updated"

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")

# param = (1, 'In Transit')
# PaymentUpdate(param)


def InProgressOrder(param):
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)

        sqlSelectQuery = """SELECT * FROM celloApp_ordertable"""
        sqlUpdateQuery = """UPDATE celloApp_ordertable SET status = "In Progress" WHERE oID = ?"""
        cursor.execute(sqlUpdateQuery, (param[0],),)
        conn.commit()
        cursor.close()
        return " Status changed to In Progress"

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")


def AbandonCustomer(param):
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)

        sqlCNameQuery = """SELECT cName FROM celloApp_ordertable WHERE oID = ?"""
        cursor.execute(sqlCNameQuery,(param[0],))
        cName = cursor.fetchone()[0]

        getOrderQuery = """SELECT orderDetails FROM celloApp_ordertable WHERE oID = ?"""
        cursor.execute(getOrderQuery,(param[0],))
        orderItem = cursor.fetchone()[0]

        sqlSelectQuery = """SELECT * FROM celloApp_ordertable"""
        sqlUpdateQuery = """UPDATE celloApp_ordertable SET status = "Abandoned" WHERE oID = ?"""
        cursor.execute(sqlUpdateQuery, (param[0],),)

        paramOrderCSV = (datetime.date.today(),cName, "Abandoned", orderItem)
        orderExit(paramOrderCSV)

        conn.commit()
        cursor.close()
        return " Customer Abndoned "

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")

# param = (8, 'In Transit')
# AbandonCustomer(param)


def CompletedCustomer(param):
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)

        getOrderQuery = """SELECT orderDetails FROM celloApp_ordertable WHERE oID = ?"""
        # print("Param : {}".format(param))
        cursor.execute(getOrderQuery,(param[0],))
        orderItem = cursor.fetchone()[0]
        orderDict = ast.literal_eval(orderItem)
        # print(orderDict)

        sqlCNameQuery = """SELECT cName FROM celloApp_ordertable WHERE oID = ?"""
        cursor.execute(sqlCNameQuery,(param[0],))
        cName = cursor.fetchone()[0]
        for key in orderDict:
            count = key

        updateProcessedQuery = """UPDATE celloApp_processed SET quantity=? WHERE color = ? AND length = ? AND width = ?;"""
        getQuantity = """SELECT quantity FROM celloApp_processed WHERE color = ? AND length = ? AND width = ?;"""
        sqlDeleteQuery = """DELETE FROM celloApp_processed WHERE LENGTH=? AND WIDTH=? AND COLOR=?;"""

        for i in range(1, key+1):                   # For checking the processed
            col = orderDict[i]['color']
            len = orderDict[i]['length']
            wid = orderDict[i]['width']
            qua = orderDict[i]['quantity']

            cursor.execute(getQuantity, (col,len,wid,),)
            if(cursor.fetchone()):
                cursor.execute(getQuantity, (col,len,wid,),)
                old_qua = cursor.fetchone()[0]
            else:
                old_qua = 0

            # print(old_qua)

            if old_qua < qua:
                return "Not enough Processed Tapes"

        for i in range(1, key+1):                  # Updating Processed
            col = orderDict[i]['color']
            len = orderDict[i]['length']
            wid = orderDict[i]['width']
            qua = orderDict[i]['quantity']

            cursor.execute(getQuantity, (col,len,wid,),)
            old_qua = cursor.fetchone()[0]

            if old_qua >= qua:
                new_qua = old_qua - qua
                # print(new_qua)
                if new_qua>0:
                  cursor.execute(updateProcessedQuery, (new_qua,col,len,wid,),)
                else:
                    cursor.execute(sqlDeleteQuery, (len,wid,col,),)
                desc = "Customer - " + cName
                paramProcess = (datetime.date.today(),desc,'',qua,col,wid,len)
                appendProcessed(paramProcess)
                paramOrderCSV = (datetime.date.today(),cName, "Completed", orderItem )
                orderExit(paramOrderCSV)
            else:
                return "Not enough Processed Tapes"

        sqlUpdateQuery = """UPDATE celloApp_ordertable SET status = "Completed" WHERE oID = ?"""
        cursor.execute(sqlUpdateQuery, (param[0],),)

        conn.commit()
        cursor.close()
        return "Updated in Processed"

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")

# param = (7, 'In Transit')
# CompletedCustomer(param)


# def chkPay(param):
#     try:
#         conn = LocalDB()
#         print("SQL Connected! Vetriiii")
#         cursor = conn.cursor(prepared=True)
#         chkStatusQuery = """SELECT payment FROM celloApp_ordertable WHERE oID = ?"""
#         cursor.execute(chkStatusQuery,(param,),)
#         pay = cursor.fetchone()
#         if pay==None:
#             return None
#         conn.commit()
#         cursor.close()
#         return pay[0]
#
#     except sqlite3.Error as error:
#         print("Errrrrror : ", error)
#
#     finally:
#         if(conn):
#             conn.close()
#             print("Disconnected")
#
# # chkPay(1)


def addCustomerNewTable(param):
    #param = (cName, address, email, gstIN)
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)

        insertQuery = """INSERT INTO celloApp_customermaster (cID, cName, address, email, gstIN) VALUES (?,?,?,?,?)"""

        pkQuery = """SELECT cId FROM celloApp_customermaster ORDER BY cID"""
        cursor.execute(pkQuery)
        oldPkArr = cursor.fetchall()
        # print(oldPkArr)

        if oldPkArr==[]:
            oldPk = 0
        else:
            oldPk = oldPkArr[-1][0]

        param = (oldPk+1,) + param

        cursor.execute(insertQuery,param,)

        sqlSelectQuery = """SELECT * FROM celloApp_customermaster"""
        # cursor.execute(sqlSelectQuery)
        # print(cursor.fetchall())

        conn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")

# addCustomerNewTable(('Aditya Srinivas', '2/B, Goriku Street, Jabbu street, Theruchi - 620008', 'basaditya@hero.com', '234FIVJF3485555'))


def returnListCustomerName():
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)

        list1 = []

        sqlSelectQuery = """SELECT cName FROM celloApp_customermaster"""

        cursor.execute(sqlSelectQuery)
        for items in cursor.fetchall():
            tup = (items[0], items[0])
            list1.append(tup)

        return list1

        conn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")

# list = returnListCustomerName()
# print(list)


def resetAll():
    try:
        conn = LocalDB()
        print("SQL Connected! Vetriiii")
        cursor = conn.cursor(prepared=True)

        truncateQuery1 = """TRUNCATE TABLE celloApp_cellotypes;"""
        truncateQuery2 = """TRUNCATE TABLE celloApp_customermaster;"""
        truncateQuery3 = """TRUNCATE TABLE celloApp_logintable;"""
        truncateQuery4 = """TRUNCATE TABLE celloApp_ordertable;"""
        truncateQuery5 = """TRUNCATE TABLE celloApp_processed;"""
        truncateQuery6 = """TRUNCATE TABLE celloApp_temptableorder;"""
        truncateQuery7 = """TRUNCATE TABLE celloApp_temptableprocess;"""
        truncateQuery8 = """TRUNCATE TABLE celloApp_userstable;"""

        cursor.execute(truncateQuery1)
        cursor.execute(truncateQuery2)
        cursor.execute(truncateQuery3)
        cursor.execute(truncateQuery4)
        cursor.execute(truncateQuery5)
        cursor.execute(truncateQuery6)
        cursor.execute(truncateQuery7)
        cursor.execute(truncateQuery8)

    except sqlite3.Error as error:
        print("Errrrrror : ", error)

    finally:
        if(conn):
            conn.close()
            print("Disconnected")

# resetAll()
