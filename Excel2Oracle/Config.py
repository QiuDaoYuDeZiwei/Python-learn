#coding= utf-8

u"""
CONFIG
AUTHOR:SYY
################################################################################
按照需求可以修改:
1.数据库信息
2.目标文件地址
2.Excel表的名称-字典:ExcelTableName_dict
3.oracle表的名称-字典:TableName_dict
4.表字段字段-字典: ColsName_dict
5.输入时的提示语句-InputStatement
################################################################################
"""

import re
import os
import time
import codecs
import cx_Oracle
import pandas as pd
from sqlalchemy import create_engine


# 数据库信息
oracle_connect = 'system/Syy19930119@localhost:1521/test'
# 格式:user/passwords@host:port/database
engine = create_engine('oracle+cx_oracle://system:Syy19930119@test', echo=True)
#create_engine(u'oracle+cx_oracle://localhost:1521/orcl', echo=True, user='<>', password='<>', dsn='<>')
chunksize = 250
# 目标文件地址
#path = ur'G:\DataToOracle'

# Excel表的名称
ExcelTableName_dict = {1: u'全省充电数据', 2: u'充电桩故障监测', 3: 'test', }

# oracle表的名称
TableName_dict = {1: 'CHARGE_REPORT', 2: 'FAULT_LIST', 3: 'test', }

# 表字段字段
# ColsName_dict = {
# u'单位': 'PROPERTY_DEPARTMENT' ,
# u'DECODE((SELECTSUBSTR(ELEC_TYPE': 'ELEC_TYPE',
# u'地址': 'ADDRESS',
# u'电价': 'ELECTRICITY_PRICE' ,
# u'户号': 'ACCOUNT_ID' ,
# u'户名': 'ACCOUNT_NAME' ,
# u'(SELECTSUM(T_SETTLE_PQ)FROMARC': 'TRADE_ELECTRICITY' ,
# u'设施类型': 'FACILITY_TYPE',
# u'所属单位': 'SUBORDINATE_DEPARTMENTS',
#}

# 输入时的提示语句
InputStatement = u"""
Enter Number:\n
1-充电数据(社会充电数据)-CHARGE_REPORT \n
2-故障工单(充电桩故障监测)-FAULT_LIST \n
3-test-test \n
Enter: """

# SQL_dict = {1: "",
# 2: "",
# 3: "select from tmp", }


