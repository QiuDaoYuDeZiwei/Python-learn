#coding= utf-8

u"""
prework
AUTHOR:SYY
################################################################################
主要内容：
1 输入目标文件目录、Excel文件导入到oracle的表名称(默认oracle中表已建。)
2 从目标文件目录下寻找后缀为 .xls or xlsx
3 将目标Excel 中的字段保存到oracle表 EXCELCOLSNAME
4 根据oracle表 EXCELCOLSNAME 更新config 中的 ColsName_dict ##手工修改！
################################################################################
"""
print __doc__

import re
import os
import time
import codecs
import cx_Oracle
import pandas as pd
from Config import *

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'


def BFS_Dir(path, TableNum, dirCallback=None, fileCallback=None):
    # 从目标文件目录下寻找后缀为 .xls or xlsx，
    # 选择需要导入的Excel表(部分是不需要导入的)
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

    pattern = ur'.*%s.*(xlsx|xls)$' % (ExcelTableName_dict[TableNum])
    ret = [i for i in ret if re.search(pattern, i)]
    return ret


def ExcelToOracle_EXCELCOLSNAME(filepath, TableNum):
    conn = cx_Oracle.connect(oracle_connect)
    cur = conn.cursor()

    tmp = pd.read_excel(filepath)
    Excel_ColName = list(tmp.columns)

    # save the excel column name
    try:
        sql = """
        create table excelcolsname (TableNum varchar2(200),filepath varchar2(200), colname varchar2(200),deal_colname varchar2(200)\
        ,constraint p primary key( colname ))
        """
        cur.execute(sql)
        conn.commit()

    except:
        print 'TABLE EXCELCOLSNAME IS ALREADY EXISTS !'
    for ColName in Excel_ColName:
        try:
            sql = "insert into EXCELCOLSNAME values ( '%s','%s' , '%s',%s)" % (
                TableNum, filepath, ColName, 'Null')
            cur.execute(sql)
            conn.commit()
        except cx_Oracle.IntegrityError:
            pass
    cur.close()
    conn.close()


def UpdateEXCELCOLSNAME(deal_case=0):
    print u"""
更新oracle中表EXCELCOLSNAME的ColName(原始excel中的列名)
可以在数据库中更新,也可以在此处更新。
默认是在数据库。若需要在此更新,deal_case=1
这里需要考虑数据类型,一般都是varchar2(200),但是日期格式的需要修改为date.
建议需修改日期格式的字段后缀统一为 _DATE,方便后面处理！！！
    """
    if deal_case != 0:
        conn = cx_Oracle.connect(oracle_connect)
        cur = conn.cursor()
        cur.execute('select * from EXCELCOLSNAME where deal_colname is null')
        tmp = cur.fetchall()
        for i in tmp:
            input_name = raw_input(u'ColName = %s, deal_colname:\n' % (
                i[1])).decode(sys.stdin.encoding)
            # 注意编码问题 电动汽车是utf-8  python是utf-8 ,但是
            sql = "update EXCELCOLSNAME set %s = '%s' where %s = '%s' " % (
                'deal_colname', input_name, 'ColName', i[1])
            cur.execute(sql)
            conn.commit()
        cur.close()
        conn.close()


def FecthDealcolname():
    conn = cx_Oracle.connect(oracle_connect, encoding="utf-8")
    cur = conn.cursor()

    cur.execute(
        'select ColName ,deal_colname from EXCELCOLSNAME where deal_colname is not null')
    try:
        tmp = dict([(i[0].decode('utf-8', 'ignore'), i[1])
                    for i in cur.fetchall()])  # 编码问题？
    except Exception as e:
        print e.message
    cur.close()
    conn.close()

    return tmp


def Prework():
    while True:
        try:
            TableNum = input(InputStatement)
            filepath_list = BFS_Dir(path, TableNum)
            break
        except:
            print 'error,please try again !'

    for i in filepath_list:
        ExcelToOracle_EXCELCOLSNAME(i)

    UpdateEXCELCOLSNAME(1)
