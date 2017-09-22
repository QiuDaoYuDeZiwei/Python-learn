#coding= utf-8

u"""
AUTHOR:SYY
主要内容：
1 输入目标文件目录、Excel文件导入到oracle的表名称(默认oracle中表已建。)
2 从目标文件目录下寻找后缀为 .xls or xlsx，并选择需要导入的Excel表(部分是不需要导入的)
3 把2中的Excel 另存为 .csv (方便后面处理)
4 将 .csv文件 导入到本地的oracle的表
##5 由于需要把本机的数据放到电能公司的电脑，需将数据导出为 .csv
"""
print __doc__

import re
import os
import time
import codecs
import cx_Oracle
import pandas as pd

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


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


def TransTableType(filepath):
    # excel 到 csv
    tmp = pd.read_excel(filepath)
    filepath = os.path.splitext(filepath)[:-1][0] + r'.csv'
    tmp.to_csv(filepath, index=False, header=False, encoding="utf-8")
    return filepath


def FileToOracle(filepath, TableNum):
    # csv 到 oracle
    # 一部分表是不需要做变动的,另一部分需要。
    conn = cx_Oracle.connect('system/Syy19930119@localhost:1521/orcl')
    cur = conn.cursor()
    try:
        cur.execute('select * from %s  where rownum <= 1 ' %
                    (TableName_dict[TableNum]))
        colsnum = len(cur.fetchone())
    except:
        print 'Table %s has no data' % (TableName_dict[TableNum])
        tmp = pd.read_csv(filepath, header=None)
        colsnum = len(tmp.columns)

    if TableNum <> 2:
        for index, line in enumerate(codecs.open(filepath, "r", "utf-8")):
            sql = """insert into  %s  values (""" % (TableName_dict[TableNum])
            for fields in (line.split(","))[0:colsnum]:
                sql = sql + "'" + fields + "',"
            print sql[:-1] + ")"
            cur.execute(sql[:-1] + ")")
            conn.commit()
        cur.close()
        conn.close()
    elif TableNum == 2:
        d = '20170' + re.search(r'.*?(\d).*?', filepath).group(1)
        for index, line in enumerate(codecs.open(filepath, "r", "utf-8")):
            sql = """insert into  %s values (""" + "'" + \
                d + "'," % (TableName_dict[TableNum])
            for fields in (line.split(","))[0:colsnum]:
                sql = sql + "'" + fields + "',"
            # sql = sql[:-1] + ",date'" + \
            #    time.strftime('%Y-%m-%d', time.localtime(time.time())) + "'" + ")"
            sql = sql[:-1] + "'" + ")"
            print sql
            # f = codecs.open(
            #   ur'D:\WORK\电能\DataToOracle\insert_sql.sql', "a+", "utf-8")
            #f.writelines(sql + ';' + '\n')
            cur.execute(sql)
            conn.commit()
        cur.close()
        conn.close()
        # f.close()


if __name__ == '__main__':

    ExcelTableName_dict = {1: u'故障工单', 2: u'充值记录'}
    TableName_dict = {1: 'FAULT_LIST', 2: 'CHARGE_REPORT'}

    TableNum = input(u"""
    enter number:\n
    1-故障工单-FAULT_LIST  \n
    2-充值记录(社会充电记录)-CHARGE_REPORT \n
    """)

    path = ur'G:\DataToOracle\国网'

    filepath_list = BFS_Dir(path, TableNum)

    csvpath_list = []
    for filepath in filepath_list:
        csvpath_list.append(TransTableType(filepath))

    for csvpath in csvpath_list:
        FileToOracle(csvpath, TableNum)

    print time.strftime('%Y-%m-%d', time.localtime(time.time()))
