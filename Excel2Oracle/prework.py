#coding= utf-8

u"""
filename:prework.py
AUTHOR:SYY
targer:pre work for Excel2Oracle
################################################################################
Content:
1 BFS_Dir(path, TableNum, dirCallback=None, fileCallback=None)
2 ColName_Excel2Oracle_EXCELCOLSNAME(filepath, TableNum)
3 UpdateEXCELCOLSNAME()
4 Createdict_ColName_Ori_Dealed()
5 CreateTable_TargetTable()

ps:
path:输入的目录地址
filepath:excel表或csv表的地址
TableNum:Config Excel表名序号和oracle表名序号
ColName:excel表的列名
deal_colname:处理后的表的列名
################################################################################
"""
# print __doc__

from Config import *

#设置编码
import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'


def BFS_Dir(path, TableNum, dirCallback=None, fileCallback=None):
    u"""
    target: \n
    广度遍历寻找文件 \n
    在path下寻找Excel表(后缀为xls or xlsx), \n
    并根据TableNum, 从Config的字典:ExcelTableName_dict \n
    选择符合条件的Excel表,返回相应的Excel表的文件地址(list).
    """
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


def ColName_Excel2Oracle_EXCELCOLSNAME(filepath, TableNum):
    u"""
    target:\n
    保存excel列名到oracle EXCELCOLSNAME
    insert into EXCELCOLSNAME values
    TableNum,filepath,colname,Null(dealed colname) \n
    return Excel_ColName(list)
    """
    conn = cx_Oracle.connect(oracle_connect)
    cur = conn.cursor()

    tmp = pd.read_excel(filepath)
    Excel_ColName = list(tmp.columns)

    try:
        #colname:excel table's columns'names
        #Null:deal_colname(dealed colname) = Null
        sql = """
        create table excelcolsname (TableNum varchar2(200),filepath varchar2(200), colname varchar2(200),deal_colname varchar2(200)\
        ,constraint p primary key(TableNum, colname ))
        """
        cur.execute(sql)
        conn.commit()
    except:
        print 'TABLE EXCELCOLSNAME IS ALREADY EXISTS !'

    for ColName in Excel_ColName:
        try:
            sql = "insert into EXCELCOLSNAME values ('%s', '%s', '%s', %s)" % (
                TableNum, filepath, ColName, 'Null')
            cur.execute(sql)
            conn.commit()
        except cx_Oracle.IntegrityError:
            #插入失败,EXCELCOLSNAME 主键的原因.
            #colname 只能对应一个 deal_colname
            pass
    cur.close()
    conn.close()
    return Excel_ColName


def UpdateEXCELCOLSNAME(TableNum):
    print u"""
    更新oracle中表EXCELCOLSNAME中 %s 的ColName
    可以在数据库中更新,也可以手动输入更新.
    若需在数据库中更新,输入0
    建议需修改日期格式的字段的后缀统一为 _DATE,方便后面处理!!!
    """ %(TableName_dict[TableNum])
    while True:
        try:
            deal_case = input(u"在数据库中更新:0 \n手动输入更新:1 \nEnter: ")
            break
        except:
            print 'error,please try again!'

    if deal_case != 0:
        conn = cx_Oracle.connect(oracle_connect)
        cur = conn.cursor()
        sql = 'select * from EXCELCOLSNAME where deal_colname is null and TableNum = %s' %(TableNum)
        cur.execute(sql)
        tmp = cur.fetchall()
        for i in tmp:
            input_name = raw_input(u'ColName = %s, deal_colname:\n  Enter:' % (
                i[2])).decode(sys.stdin.encoding)
            # 注意编码问题 电动汽车是utf-8  python是utf-8
            sql = "update EXCELCOLSNAME set %s = '%s' where %s = '%s' and  TableNum = %s" % (
                'deal_colname', input_name, 'ColName', i[2], TableNum)
            cur.execute(sql)
            conn.commit()
        cur.close()
        conn.close()
    #return bool(deal_case)

def Createdict_ColName_Ori_Dealed(TableNum):
    u"""
    target:\n
    从EXCELCOLSNAME取TableNum = %s
    ColName,deal_colname,构建字典{ColName:deal_colname}
    return tmp(dict)
    """ %(TableNum)

    conn = cx_Oracle.connect(oracle_connect, encoding="utf-8")
    cur = conn.cursor()
    cur.execute(
        'select ColName ,deal_colname from EXCELCOLSNAME where deal_colname is not null and TableNum = %s' %(TableNum))
    try:
        tmp = dict([(i[0].decode('utf-8', 'ignore'), i[1])
                    for i in cur.fetchall()])  # 编码问题
    except Exception as e:
        print e.message
    cur.close()
    conn.close()
    return tmp


def CreateTable_TargetTable(TableNum):
    u"""
    target:\n
    input 0/1
    if 1:
        drop table TableName_dict[TableNum]
    create table TableName_dict[TableNum]
    """

    conn = cx_Oracle.connect(oracle_connect, encoding="utf-8")
    cur = conn.cursor()

    cur.execute("select 1 from ALL_ALL_TABLES where table_name = '%s' " %(TableName_dict[TableNum].upper()))
    t = cur.fetchall()
    
    if bool(t):
        DropCase = input(u'Need to Drop Table %s\n 0-No 1-Yes\nEnter:' %
                         (TableName_dict[TableNum]))
        if DropCase == 1:
            DropCase2 = input(
                u'Careful! Now Droping Table!\n Sure? %s \n 0-No 1-Yes \n Enter:' % (TableName_dict[TableNum]))
            if DropCase2 == 1:
                cur.execute('Drop Table %s' % (TableName_dict[TableNum]))
                conn.commit()

    cur.execute(
        "select deal_colname from EXCELCOLSNAME where deal_colname is not null and TableNum = %s" % (TableNum))
    deal_colname = cur.fetchall()

    if TableNum == 1:
        #1-充电数据(社会充电数据)-CHARGE_REPORT 缺少日期
        sql = "create table %s" % (TableName_dict[TableNum]) + ' ( '
        sql += 'CHARGE_MONTH date, '
    else:
        sql = "create table %s" % (TableName_dict[TableNum]) + ' ( '

    for i in deal_colname:
        if re.match(r'.*_DATE$', i[0]):
            sql += i[0] + ' date ,'
        else:
            sql += i[0] + ' varchar2(200) ,'
    sql += ' DT date)' # DT 更新时间
    try:
        cur.execute(sql)
        conn.commit()
    except cx_Oracle.DatabaseError:
        print 'error Table %s IS ALREADY EXISTS!' % (TableName_dict[TableNum])

    cur.close()
    conn.close()


# def Prework(TableNum):
#     # while True:
#         # try:
#             #TableNum = input(InputStatement)
#             #filepath_list = BFS_Dir(path, TableNum)
#             # break
#         # except:
#             # print 'error,please try again !'
#
#     filepath_list = BFS_Dir(path, TableNum)
#
#     for i in filepath_list:
#         ColName_Excel2Oracle_EXCELCOLSNAME(i, TableNum)
#
#     UpdateEXCELCOLSNAME()
#     DealCase = input('Update is done? \n 0-NO \n 1-Yes \n Enter:')
#     CreateTable_Deal(TableNum)
