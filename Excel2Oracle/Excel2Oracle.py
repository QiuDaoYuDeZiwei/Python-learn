#coding= utf-8

u"""
filename:Excel2Oracle.py
AUTHOR:SYY
target:input path,TableNum,insert into target_table(database oracle) data.
################################################################################
Content:
1 输入目标文件目录path,
    Excel表名序号和oracle表名序号 TableNum
    ##参考config的字典：ExcelTableName_dict,字典：TableName_dict

2 在目标文件目录path下寻找Excel表(后缀为xls or xlsx)
    ,并选择符合条件的Excel表,返回 Excel表的文件地址(list).
    ## 部分是不需要导入的,根据名称片段来判断的ExcelTableName_dict[TableNum]
    ##例 文件目录下仅需导入 充值记录的,桩明细不需要.

3 判断2中得到的list的excel表列名是否都已经在数据库表EXCELCOLSNAME更新存在了;
if False:
    ##EXCELCOLSNAME Colnums:TableNum,filepath,列名,deal_colname(Null)
    将excel表的TableNum,filepath,colname,Null  插入 EXCELCOLSNAME;
    选择在窗口手动输入或在数据库表EXCELCOLSNAME 更新
    ##需要注意日期格式字段的命名!建议以 _DATE 为后缀

  判断2中的excel是否已经转化为csv(方便后面处理)
if False:
    Excel 另存为 csv
  将csv文件导入到本地的oracle的临时表tmp

4 try create table TableName_dict[TableNum]
    ##字段选择EXCELCOLSNAME中TableNum中的全部字段.
    ##注意日期格式后缀为 _DATE.建表和插值时需要注意这一点.
    ##另外需新增字段DT date,作为更新时间的字段.

5 从临时表tmp 选取字段插值目标表TableName_dict[TableNum].
    ##需要注意日期格式的问题.

################################################################################
"""
print __doc__

from prework import *

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'


def ExcelToOracle_tmp(filepath, TableNum):
    u"""
    target:\n
    读取filepath的文件, \n
    按照Createdict_ColName_Ori_Dealed(TableNum)的dict修改列名, \n
    在oracle 新建表tmp,保存数据到表tmp. \n
    return (flag,Tabletmp_ColName,ColsName_dict_ori.values())
    (tuple;bool,list,list)
    """
    flag = 0 #是否需要修改oracle的目标表

    conn = cx_Oracle.connect(oracle_connect)
    cur = conn.cursor()

    Excel_ColName = ColName_Excel2Oracle_EXCELCOLSNAME(filepath, TableNum)

    ColsName_dict_ori = Createdict_ColName_Ori_Dealed(TableNum)

    Tabletmp_ColName = [ColsName_dict_ori[i]
                     for i in Excel_ColName if i in ColsName_dict_ori.keys()]

    print len(Excel_ColName) , len(Tabletmp_ColName)
    while len(Excel_ColName) > len(Tabletmp_ColName):
        UpdateEXCELCOLSNAME(TableNum)
        ColsName_dict = Createdict_ColName_Ori_Dealed(TableNum)
        Tabletmp_ColName = [ColsName_dict[i]
                     for i in Excel_ColName if i in ColsName_dict.keys()]
        print len(Excel_ColName) , len(Tabletmp_ColName)

        if len(set(ColsName_dict_ori.values())) < len(set(ColsName_dict.values())) and len(ColsName_dict_ori.values()) > 0 :
            flag = 1
    try:
        cur.execute('drop table tmp')
        conn.commit()
    except:
        pass
    # Create Table tmp
    CreateTabletmp_sql = 'create table tmp ( '
    for i in set(Tabletmp_ColName):
        CreateTabletmp_sql += str(i) + ' VARCHAR2(200) ,'

    cur.execute(CreateTabletmp_sql[:-1] + ')')
    conn.commit()

    # excel 2 csv
    #tmp = pd.read_excel(filepath)
    #tmp.columns = Tabletmp_ColName
    #filepath = os.path.splitext(filepath)[:-1][0] + r'.csv'
    #if not os.path.exists(filepath):
        #tmp.to_csv(filepath, index=False, header=False, encoding="utf-8")

    # insert into tmp from csv's data
    ###

    tmp = pd.read_excel(filepath)
    print filepath
    tmp.columns = Tabletmp_ColName
    try:
        tmp.to_sql('tmp', engine, if_exists='append', index = False, chunksize = chunksize)
    except:
        print 'error ,please check filepath %s' % (filepath)
        print 'usually ,filepath columns have None'
        return None
    #for index, line in enumerate(codecs.open(filepath, "r", "utf-8")):
        #sql = """insert into tmp values ("""
        #for fields in (line.split(",")):
            #sql = sql + "'" + fields + "',"
        ##print sql[:-1] + ")"
        #cur.execute(sql[:-1] + ")")
        #conn.commit()
    cur.close()
    conn.close()
    return (flag,Tabletmp_ColName,ColsName_dict_ori.values())


def MergeTable_Tmp_Target(filepath, TableNum):
    u""""

    """
    conn = cx_Oracle.connect(oracle_connect)
    cur = conn.cursor()

    Et = ExcelToOracle_tmp(filepath, TableNum)
    if bool(Et):
        flag = Et[0]
        Tabletmp_ColName = Et[1]
        TableName_ori = set(Et[2])
    
        cur.execute("select 1 from ALL_ALL_TABLES where table_name = '%s' " %(TableName_dict[TableNum].upper()))
        t = cur.fetchall()
    
        if flag and bool(t):
            print """Shit! Now We Have Trouble: \n
            Excel Table %s Have More Cols Than Table %s
            Filepath Is %s\n
            Now We Have 2 Solutions:
            1, Find The File, Delete Columns Which Not In Oracle Target Table;
            2, Drop Oracle Target Table,Do It Again
            """% (ExcelTableName_dict[TableNum], TableName_dict[TableNum], filepath)
    
            while True:
                try:
                    deal_case = input(u'Solution 1 OR 2 \n Enter(1 or 2):')
                    if deal_case == 1 or deal_case == 2:
                        break
                except:
                    print 'Error ,Please Try Again'
    
            if deal_case == 1:
                cur.execute('drop table tmp')
                conn.commit()
                cur.close()
                conn.close()
                print 'Bye'
            else:
                try:
                    cur.execute('drop table %s_tmp' % (TableName_dict[TableNum]) )
                    conn.commit()
                except:
                    print 'error,drop table %s_tmp' % (TableName_dict[TableNum])
                cur.execute('rename  %s to %s_tmp' %(TableName_dict[TableNum],TableName_dict[TableNum]))
                conn.commit()
                CreateTable_TargetTable(TableNum)
                sql_part1 = 'insert into %s ( ' % (TableName_dict[TableNum])
                sql_part2 = 'select '
                for i in TableName_ori:
                    sql_part1 += i + ' ,'
                    sql_part2 += i + ' ,'
                sql = sql_part1 +  ' dt ) ' + sql_part2 + 'dt from %s_tmp' % (TableName_dict[TableNum])
                cur.execute(sql)
                conn.commit()
                cur.execute('drop table %s_tmp' % (TableName_dict[TableNum]) )
                conn.commit()
    
        if not bool(t):
            CreateTable_TargetTable(TableNum)
    
    
        sql_part1 = 'insert into %s ( ' % (TableName_dict[TableNum])
        sql_part2 = 'select '
        if TableNum != 1:
            for i in set(Tabletmp_ColName):
                sql_part1 += i + ' , '
                if re.match(r'.*_DATE$',i.upper()):
                    sql_part2 += "to_date(%s,'YYYY-MM-DD HH24:MI:SS')," %(i)
                else:
                    sql_part2 += i + ' , '
        else:
            d = '2017-' + re.search(r'.*?(\d).*?', filepath).group(1) + '-1'
            sql_part1 += ' CHARGE_MONTH ,'
            sql_part2 += " to_date('%s','YYYY-MM-DD HH24:MI:SS') , " %(d)
            for i in set(Tabletmp_ColName):
                sql_part1 += i + ' , '
                if re.match(r'.*_DATE$',i.upper()):
                    sql_part2 += "to_date(%s,'YYYY-MM-DD HH24:MI:SS') , " %(i)
                else:
                    sql_part2 += i + ' , '
        sql_part1 = sql_part1 + 'DT )'
        sql_part2 = sql_part2 + 'SYSDATE from tmp'
        sql = sql_part1 + sql_part2
        print sql
        cur.execute(sql)
        conn.commit()
        cur.execute('drop table tmp')
        conn.commit()
    
        cur.close()
        conn.close()


if __name__ == '__main__':

    while True:
        try:
            path = raw_input('Enter Path: ').decode(sys.stdin.encoding).strip()
            TableNum = input(InputStatement)
            filepath_list = BFS_Dir(path, TableNum)
            if bool(filepath_list):
                break
        except:
            print 'error,please try again!'

    for filepath in filepath_list:
        #ExcelToOracle_tmp(filepath, TableNum)
        MergeTable_Tmp_Target(filepath, TableNum)

    print time.strftime('%Y-%m-%d', time.localtime(time.time())) + ' ok'
