#coding= utf-8

import random
import MySQLdb
from config import get_header
from MySQLHelper import MySQLHelper
from CrawlNovel import *
from TestProxies import TestProxy


def fetchproxies():
    count = 15
    DB_CONFIG = {
        'host': 'localhost',
        'password': '123456',
        'charset': 'utf8',
        'use': 'yy',
        'database': 'proxy'
    }
    con = MySQLdb.connect(DB_CONFIG['host'], DB_CONFIG['use'], DB_CONFIG['password'],
                               DB_CONFIG['database'], charset=DB_CONFIG['charset'])
    cursor = con.cursor()
    cursor.execute('SET NAMES utf8;')
    con.commit()
    sql =  'select ip,port from proxys where protocol = 0 order by score'
    cursor.execute(sql)
    results = cursor.fetchall()
    con.close()

    proxies = []
    for i in results:  # i is a tuple ('http://218.106.98.166:53281',)
        proxy_host = 'http://' + str(i[0]) + ':' + str(i[1])
        proxy_temp = {"http": proxy_host}
        print proxy_temp
        if TestProxy(proxy_temp):
            proxies.append(proxy_temp)
        if len(proxies) >= count:
            return proxies

def NovelCrawl_Main(count):
    url = r'http://www.yousuu.com/booklist'
    proxies = fetchproxies()
    for i in range(count):
        try:
            header=get_header()
            proxy = random.choice(proxies)
            url=CrawlNovelList(url,header,proxy)
        except Exception as e:
            print 'error'
            print e.message
            pass

    sql='select distinct novellisturl from pagenovel '
    a=MySQLHelper()
    NovelListUrl = a.SqlFecthAll(sql)
    a.CloseCon()
    print len(NovelListUrl)

    #proxies = fetchproxies()
    for i in NovelListUrl:
        try:
            header=get_header()
            proxy = random.choice(proxies)
            print i[0]
            CrawlNovel(i[0],header,proxy)
        except Exception as e:
            print 'error'            
            print e.message
            pass

    a=MySQLHelper()
    sql='select distinct novelurl from novelurl'
    NovelUrl = a.SqlFecthAll(sql)
    a.CloseCon()
    print len(NovelUrl)

    #proxies = fetchproxies()
    for i in NovelUrl:
        try:
            header=get_header()
            proxy = random.choice(proxies)
            print i[0]            
            CrawlNovelData(i[0],header,proxy)
        except Exception as e:
            print 'error'            
            print e.message
            pass
      
if __name__ == '__main__':
    NovelCrawl_Main(10)
