import cx_Oracle

username = 'sys'
password = '123456789CCC'
ip = 'localhost'
port = 1521
SID = 'xe'
dsn_tns = cx_Oracle.makedsn(ip, port, SID)
encoding = 'UTF-8'

