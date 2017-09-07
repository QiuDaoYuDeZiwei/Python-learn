#coding= utf-8

import re
import time
import cx_Oracle
from MySQLHelper import MySQLHelper

a = MySQLHelper()
sql = 'select * from fun.noveldata order by rundate desc '
rawdata = a.SqlFecthAll(sql)
a.CloseCon()



conn = cx_Oracle.connect('system/Syy19930119@localhost:1521/orcl')
cursor = conn.cursor()

try:
    cursor.execute('drop table SYY_NOVELDATA')
except:
    pass

sql = """
    CREATE TABLE system.SYY_NOVELDATA (\
    RUNDATE DATE\
    ,NOVELURL  VARCHAR2(250)\
    ,NOVELNAME VARCHAR2(250)\
    ,NOVEL_ORGURL VARCHAR2(250)\
    ,TAG_CATEGORY VARCHAR2(250)\
    ,AUTHOR  VARCHAR2(250)\
    ,NOVELRANK  VARCHAR2(250)\
    ,WORLDCOUNT  VARCHAR2(250)\
    ,SECTIONCOUNT  VARCHAR2(250)\
    ,DATASOURCE VARCHAR2(250)\
    ,NOVELUPDATETIME VARCHAR2(250)\
    ,LASTEETSECTION VARCHAR2(250)\
    ,PRIMARY KEY (NOVELURL, NOVELNAME) )"""
cursor.execute(sql)
conn.commit()

for row in rawdata:
    row = list(row)
    #t = [i.strip() for i in re.split(r'(?:\.*:) ',re.sub(r'(?<=\s\s)(.*?)(?=\:)','',row.pop() ), 6 )[2:] ]
    t = [i.strip() for i in  re.split(r'\s*', re.sub(r'(\s*\S*\:)','', row.pop()), 6)[2:] ]
    row.extend(t)
    cursor.execute("insert into   SYY_NOVELDATA  values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12)", row)
    conn.commit()
cursor.close()
conn.close()
print 1
