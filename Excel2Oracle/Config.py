#coding= utf-8

u"""
CONFIG
AUTHOR:SYY
################################################################################
按照需求可以修改：
1.数据库信息
2.目标文件地址
2.Excel表的名称-字典：ExcelTableName_dict
3.oracle表的名称-字典：TableName_dict
4.表字段字段-字典: ColsName_dict
5.输入时的提示语句-InputStatement
################################################################################
"""
# 数据库信息
oracle_connect = 'system/Syy19930119@localhost:1521/test'
# 格式：user/passwords@host:port/database

# 目标文件地址
path = ur'G:\DataToOracle'

# Excel表的名称
ExcelTableName_dict = {1: u'故障工单', 2: u'充电数据', 3: 'test', }

# oracle表的名称
TableName_dict = {1: 'FAULT_LIST', 2: 'CHARGE_REPORT', 3: 'test', }

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
enter number:\n
1-故障工单-FAULT_LIST  \n
2-充电数据(社会充电数据)-CHARGE_REPORT \n
3-test-test\n
"""

SQL_dict = {1: "",
            2: "",
            3: "select from tmp", }
