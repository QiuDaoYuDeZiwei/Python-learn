#coding= utf-8
__author__ = 'syy'

import time
from MySQLHelper import MYSQLHelper


class TABLEipHelper(MYSQLHelper):

    def TruncTableIP(self):
        self.cursor.execute("TRUNCATE TABLE ip")
        self.con.commit()

    def DropTableIP(self):
        self.cursor.execute("DROP TABLE IF EXISTS ip")
        self.con.commit()

    def CreateTableIP(self):
        sql = """CREATE TABLE if NOT exists ip (
            timegot datetime DEFAULT NULL,
            type varchar(10) DEFAULT NULL,
            ip varchar(50) NOT NULL,
            PRIMARY KEY (ip) )
            ENGINE=InnoDB DEFAULT CHARSET=utf8
            """
        self.cursor.execute(sql)
        self.con.commit()

    def InsertIP(self, proxy):
        """proxy is a dict"""
        sql = """replace into ip values ('%s','%s' ,'%s') """ \
            % (time.strftime('%Y-%m-%d %X', time.localtime(time.time())), proxy.keys()[0], proxy.values()[0])
        self.cursor.execute(sql)
        self.con.commit()


class TABLEzhipinHelper(MYSQLHelper):

    def DropTablezhipin(self):
        sql = 'drop table if exists zhipin'
        self.cursor.execute(sql)
        self.con.commit()

    def CreateTablezhipin(self):
        sql = """CREATE TABLE IF NOT EXISTS zhipin (
            dd int ,
            date datetime,
            base text,
            title  text ,
            pay  text,
            message text,
            companyname text,
            companymessage text,
            detail_url text )
            DEFAULT CHARSET=utf8
            PARTITION  BY RANGE(dd) (
            PARTITION  p0 VALUES LESS THAN  (5),
            PARTITION  p1 VALUES LESS THAN  (10),
            PARTITION  p2 VALUES LESS THAN  (15),
            PARTITION  p3 VALUES LESS THAN  (20),
            PARTITION  p4 VALUES LESS THAN  (25),
            PARTITION  p5  VALUES LESS THAN MAXVALUE  )"""
        self.cursor.execute(sql)
        self.con.commit()

    def Insertzhipin(self, detail):
        """
        proxy is a dict
        """
        sql = """insert into zhipin values ('%s','%s','%s' ,'%s','%s','%s','%s','%s','%s') """ \
            % (time.strftime('%d', time.localtime(time.time())),
               time.strftime(
                   '%Y-%m-%d %X', time.localtime(time.time())), u'Hangzhou', detail[0],
               detail[1], detail[2], detail[3],
               detail[4], detail[5])
        self.cursor.execute(sql)
        self.con.commit()
