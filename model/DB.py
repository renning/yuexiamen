# -*- encoding:utf8 -*-
'''
@author: dove
@version: 2014-06-10

封装的mysql常用函数
'''

import MySQLdb
import MySQLdb.cursors

class DB():
    def __init__(self, **args):
        print args
        self.DB_HOST = args.get('DB_HOST')
        self.DB_PORT = args.get('DB_PORT')
        self.DB_USER = args.get('DB_USER')
        self.DB_PWD = args.get('DB_PWD')
        self.conn = self.getConnection()

    def getConnection(self):
        return MySQLdb.Connect(
                           host=self.DB_HOST, #设置MYSQL地址
                           port=self.DB_PORT, #设置端口号
                           user=self.DB_USER, #设置用户名
                           passwd=self.DB_PWD, #设置密码
                           charset='utf8', #设置编码
                           cursorclass=MySQLdb.cursors.DictCursor
                           )

    def query(self, sqlString):
        cursor=self.conn.cursor()
        cursor.execute(sqlString)
        returnData=cursor.fetchall()
        cursor.close()
        self.conn.close()
        return returnData

    def update(self, sqlString, dt=None):
        cursor=self.conn.cursor()
        if dt:
            cursor.execute(sqlString, dt)
        else:
            cursor.execute(sqlString)
        self.conn.commit()
        cursor.close()
        self.conn.close()

    def insert(self, sqlString, dt=None):
        self.update(sqlString, dt)

if __name__=="__main__":
    db=DB('127.0.0.1',3306,'root','','wordpress')
    print db.query("show tables;")
