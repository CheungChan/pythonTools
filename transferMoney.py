#coding:utf-8
import sys
import MySQLdb


class TransferMoney(object):

    def __init__(self, conn):
        self.conn = conn
        
    def checkIdAvailable(self, trans_id):
        sql = "select * from transferMoney where id=%s"%trans_id
        print "sql:"+sql
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            rs = cursor.fetchall()
            if len(rs) !=1:
                raise Exception("账号%s不存在"%trans_id)
        finally:
            cursor.close()
    
    def checkEnoughMoney(self, trans_id, money):
        sql = "select * from transferMoney where id=%s and money>=%s"%(trans_id,money)
        print "sql:"+sql
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("账号%s余额不足"%trans_id)
        finally:
            cursor.close()
    
    def reduceMoney(self, trans_id, money):
        sql = "update transferMoney set money=money-%s where id=%s"%(money,trans_id)
        print "sql:"+sql
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            if cursor.rowcount != 1:
                raise Exception("账号%s没有足够的钱"%trans_id)
        finally:
            cursor.close()
    
    def addMoney(self, trans_id, money):
        sql = "update transferMoney set money = money+%s where id=%s"%(money,trans_id)
        print "sql:"+sql
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            if cursor.rowcount != 1:
                raise Exception("账号%s充钱失败"%trans_id)
        finally:
            cursor.close()

    
    def checkBothMoney(self, source_trans_id, target_trans_id):
        sql = "select money from transferMoney where id=%s"
        sql_source = sql%source_trans_id
        sql_target = sql%target_trans_id
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql_source)
            rsc = cursor.fetchone()
            cursor.execute(sql_target)
            rst = cursor.fetchone()
            print "%s用户余额为%d,%s用户余额为%d"%(source_trans_id,int(rsc[0]),target_trans_id,int(rst[0]))
        except Exception as e:
            print e
        finally:
            cursor.close()
    
    
    def transfer(self, source_trans_id, target_trans_id, money):
        try:
            self.checkIdAvailable(source_trans_id)
            self.checkIdAvailable(target_trans_id)
            self.checkEnoughMoney(source_trans_id,money)
            self.reduceMoney(source_trans_id,money)
            self.addMoney(target_trans_id,money)
            self.checkBothMoney(source_trans_id,target_trans_id)
            self.conn.commit()
            print "转账成功"
        except Exception as e:
            print e
            self.conn.rollback()
            print "转账失败"
        finally:
            self.conn.close()
    
if __name__ == "__main__":
    source_trans_id = sys.argv[1]
    target_trans_id = sys.argv[2]
    money = sys.argv[3]
    conn = MySQLdb.Connect(host="127.0.0.1",port=3307,db="imoocpython",user="root",passwd="1234",charset="utf8")
    transmoney = TransferMoney(conn)
    transmoney.transfer(source_trans_id,target_trans_id,money)
    