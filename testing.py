import pymysql
import paramiko
import pandas as pd
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
import mysql.connector

# home = expanduser('~')
# mypkey = paramiko.RSAKey.from_private_key_file(home + pkeyfilepath)
# if you want to use ssh password use - ssh_password='your ssh password', bellow

# sql_hostname = 'localhost'
# sql_username = 'affixDashboard'
# sql_password = 'affix'
# sql_main_database = 'i7333420_wp1'
# sql_port = 3306
# ssh_host = '148.66.138.143'
# ssh_user = 'scckcqsnj9le'
# ssh_passwd = '#cPanel123'
# ssh_port = 22
# # sql_ip = '1.1.1.1.1'
#
# with SSHTunnelForwarder(
#         (ssh_host, ssh_port),
#         ssh_username=ssh_user,
#         ssh_password=ssh_passwd,
#         remote_bind_address=(sql_hostname, sql_port)) as tunnel:
#     conn = pymysql.connect(host='127.0.0.1', user=sql_username,
#             passwd=sql_password, db=sql_main_database,
#             port=tunnel.local_bind_port)
#     query = '''SELECT VERSION();'''
#     data = pd.read_sql_query(query, conn)
#
#     print(conn)
#     cursor = conn.cursor()
#     cursor.execute("SELECT table_name FROM information_schema.tables;")
#     print(cursor.fetchall())
#
#     conn.close()


conn = mysql.connector.connect(
    host="148.66.138.143",
    database="i7333420_wp1",
    user="affixDashboard",
    password="affix",
    port="3306")
print(conn)


# conn = mysql.connector.connect(host="148.66.138.143",database="i7333420_wp1",user="affixDashboard",password="affix",port="3306")
# print(conn)
