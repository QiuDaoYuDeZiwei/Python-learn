import MySQLdb
import cx_Oracle

DB_CONFIG = {
    'host': 'localhost',
    'password': '123456',
    'charset': 'utf8',
    'use': 'yy',
    'database': 'fun'
}

con = MySQLdb.connect(DB_CONFIG['host'], DB_CONFIG['use'], DB_CONFIG['password'],
                      DB_CONFIG['database'], charset=DB_CONFIG['charset'])
cursor = con.cursor()
cursor.execute('SET NAMES utf8;')
con.commit()

sql = '''SELECT * FROM fun.lianjia'''
cursor.execute(sql)
results = cursor.fetchall()  # results is a tuple
cursor.close()

conn = cx_Oracle.connect('system/Syy19930119@localhost:1521/orcl')
cursor = conn.cursor()

try:
    cursor.execute('drop table syy_lianjia')
except:
    pass

sql = """
CREATE TABLE syy_lianjia (
  idate date,
  communityname varchar(250),
  amount90 varchar(250),
  county varchar(250),
  plate varchar(250),
  builddate varchar(250),
  averageprice varchar(250),
  numberofsolds varchar(250)
)"""
cursor.execute(sql)
conn.commit()

for i in results:
    cursor.execute(
        "insert into  syy_lianjia  values (:1,:2,:3,:4,:5,:6,:7,:8)", i)
    conn.commit()
cursor.close()
conn.close()
