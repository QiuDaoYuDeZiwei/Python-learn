# coding= utf-8
import time
from MySQLHelper import MySQLHelper


class SaveNovelData(MySQLHelper):

    def InsertTablePageNovel(self, urls_tuple):
        try:
            self.cursor.execute('create table pagenovel\
            (rundate datetime,pageurl varchar(100),nextpageurl varchar(100),novellisturl varchar(100),\
            PRIMARY key (pageurl,novellisturl))\
            ENGINE=InnoDB DEFAULT CHARSET=utf8')
            self.con.commit()
        except Exception as e:
            print e.message
        sql = """replace into pagenovel values ('%s','%s' ,'%s' ,'%s') """ \
            % (time.strftime('%Y-%m-%d %X', time.localtime(time.time())), urls_tuple[0], urls_tuple[1], urls_tuple[2])
        print sql
        self.cursor.execute(sql)
        self.con.commit()

    def InsertTableNovelUrl(self, urls_tuple):
        try:
            self.cursor.execute('create table novelurl\
            (rundate datetime,novellisturl varchar(100),novelurl varchar(100),\
            PRIMARY key (novellisturl,novelurl))')
            self.con.commit()
        except Exception as e:
            print e.message
        sql = """replace into novelurl values ('%s','%s' ,'%s') """ \
            % (time.strftime('%Y-%m-%d %X', time.localtime(time.time())), urls_tuple[0], urls_tuple[1])
        print sql
        self.cursor.execute(sql)
        self.con.commit()

    def InsertTableNovelData(self, datatuple):
        try:
            self.cursor.execute('create table noveldata\
                (rundate datetime,novelurl  varchar(100),\
                 novelname varchar(100),novel_orgurl varchar(100),\
                tag_category varchar(100) ,author  varchar(100) , \
                novelrank  varchar(100) ,detail text ,\
                PRIMARY key(novelname, author))\
                ENGINE=InnoDB DEFAULT CHARSET=utf8')
            self.con.commit()
        except Exception as e:
            print e.message
        sql = """replace into noveldata values ('%s','%s','%s' ,'%s','%s','%s' ,'%s','%s')"""\
            % (time.strftime('%Y-%m-%d %X', time.localtime(time.time())), datatuple[0],
               datatuple[1], datatuple[2], datatuple[3], datatuple[4], datatuple[5], datatuple[6])
        print sql
        self.cursor.execute(sql)
        self.con.commit()
