#coding:utf-8
import MySQLdb
conn = MySQLdb.Connect(
                       host = "127.0.0.1",
                       port = 3307,
                       user = "root",
                       passwd = "1234",
                       db = "imoocpython",
                       charset = "utf8"
                       )
cursor = conn.cursor()
sql = "select * from usertable"
cursor.execute(sql)
rs = cursor.fetchall()
for row in rs:
    print "userid:%s  username:%s" % row


print conn
print cursor
cursor.close()
conn.close()