#coding= utf-8
u"""
主要内容：
1从目标文件目录下寻找后缀为 .xls or xlsx
2另存为 .csv (方便后面处理)
3将 .csv文件 导入到本地的oracle
"""


import re
import os
import cx_Oracle
import pandas as pd
import time
import codecs
# 从目标文件目录下寻找后缀为 .xls or xlsx

ddl = u"""
    DROP TABLE CHARGE_REPORT;
    CREATE TABLE CHARGE_REPORT
       (
        CHARGE_MONTH VARCHAR2(10),
        PROPERTY_DEPARTMENT VARCHAR2(100),
        ELEC_TYPE VARCHAR2(100),
        ADDRESS  VARCHAR2(200),
        ELECTRICITY_PRICE VARCHAR2(100) ,
        ACCOUNT_ID VARCHAR2(60),
        ACCOUNT_NAME VARCHAR2(100),
        TRADE_ELECTRICITY NUMBER(30,0),
        FACILITY_TYPE VARCHAR2(60),
        SUBORDINATE_DEPARTMENTS VARCHAR2(60),
        DT DATE
       ) SEGMENT CREATION IMMEDIATE
      PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 NOCOMPRESS LOGGING
      STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
      PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
      TABLESPACE "USERS" ;
"""


def BFS_Dir(path, dirCallback=None, fileCallback=None):
    queue = []
    ret = []
    queue.append(path)
    while len(queue) > 0:
        tmp = queue.pop(0)
        if(os.path.isdir(tmp)):
            # ret.append(tmp)
            for item in os.listdir(tmp):
                queue.append(os.path.join(tmp, item))
            if dirCallback:
                dirCallback(tmp)
        elif(os.path.isfile(tmp)):
            ret.append(tmp)
            if fileCallback:
                fileCallback(tmp)
    ret = [i for i in ret if re.search(ur'.*全省充电数据.*xlsx$', i)]
    return ret

# excel 到 csv
# pandas


def TransTableType(filepath):
    tmp = pd.read_excel(filepath)
    filepath = os.path.splitext(filepath)[:-1][0] + r'.csv'
    tmp.to_csv(filepath, index=False, header=False, encoding="utf-8")
    return filepath
# csv 到 oracle


def FileToOracle(filepath):
    d = '20170' + re.search(r'.*?(\d).*?', filepath).group(1)
    conn = cx_Oracle.connect('system/Syy19930119@localhost:1521/orcl')
    cur = conn.cursor()
    for index, line in enumerate(codecs.open(filepath, "r", "utf-8")):
        sql = """insert into CHARGE_REPORT values (""" + "'" + d + "',"
        for fields in (line.split(","))[0:9]:
            sql = sql + "'" + fields + "',"
        sql = sql[:-1] + ",date'" + \
            time.strftime('%Y-%m-%d', time.localtime(time.time())) + "'" + ")"
        print sql
        f = codecs.open(
            ur'D:\WORK\电能\DataToOracle\insert_sql.sql', "a+", "utf-8")
        f.writelines(sql + ';' + '\n')
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    f.close()


def main(path):
    filepath_list = BFS_Dir(path)
    csvpath_list = []
    for filepath in filepath_list:
        csvpath_list.append(TransTableType(filepath))
    for csvpath in csvpath_list:
        FileToOracle(csvpath)


if __name__ == '__main__':
    path = ur'D:\WORK\电能\DataToOracle\社会'
    main(path)
    print time.strftime('%Y-%m-%d', time.localtime(time.time()))
