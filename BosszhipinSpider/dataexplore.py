# coding= utf-8
from MySQLHelper import MYSQLHelper
import cx_Oracle

d = MYSQLHelper()
sql = 'select * from fun.zhipin'
rawdata = d.SqlFecthAll(sql)
d.CloseCon()

conn = cx_Oracle.connect('system/Syy19930119@localhost:1521/orcl')
cursor = conn.cursor()


sql = """CREATE TABLE  ZHIPIN (DD INT ,IDATE DATE,\
BASE VARCHAR2(100),TITLE  VARCHAR2(100) ,\
PAY  VARCHAR2(100),MESSAGE VARCHAR2(100),\
COMPANYNAME VARCHAR2(100),COMPANYMESSAGE VARCHAR2(100),\
DETAIL_URL VARCHAR2(100) )\
PARTITION  BY RANGE(DD) \
(PARTITION  P0 VALUES LESS THAN  (5),\
PARTITION  P1 VALUES LESS THAN  (10),\
PARTITION  P2 VALUES LESS THAN  (15),\
PARTITION  P3 VALUES LESS THAN  (20),\
PARTITION  P4 VALUES LESS THAN  (25),\
PARTITION  P5  VALUES LESS THAN (MAXVALUE))"""

try:
    cursor.execute(sql)
    conn.commit()
except Exception as e:
    print 'error: failed to create table %s ' % e.message

for i in rawdata:
    cursor.execute('insert into zhipin values (:1,:2,:3,:4,:5,:6,:7,:8,:9)', i)
    conn.commit()
cursor.close()
conn.close()
