#coding= utf-8

import threading
import random
import time
import MySQLdb
from config import get_header
from MySQLHelper import MySQLHelper
from CrawlNovel import *
from TestProxies import TestProxy


def fetchproxies(count):
    #count = 30
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
    sql = 'select ip,port from proxys where protocol = 0 order by score desc '
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


def Main_CrawlNovelList(url, count):
    #url = r'http://www.yousuu.com/booklist'
    proxies = fetchproxies(20)
    for i in range(count):
        try:
            header = get_header()
            proxy = random.choice(proxies)
            url = CrawlNovelList(url, header, proxy)
        except Exception as e:
            print 'error'
            print e.message
            pass


def Main_CrawlNovel(pp):
    sql = 'select distinct novellisturl from pagenovel order by rundate desc limit %s offset %s' % (
        150, int(pp) * 150)
    a = MySQLHelper()
    NovelListUrl = a.SqlFecthAll(sql)
    a.CloseCon()

    proxies = fetchproxies(30)
    for i in NovelListUrl:
        try:
            header = get_header()
            proxy = random.choice(proxies)
            print i[0]
            CrawlNovel(i[0], header, proxy)
        except Exception as e:
            print 'error'
            print e.message
            pass


def Main_CrawlNovelData(pp):
    sql = 'select distinct novelurl from novelurl order by rundate desc limit %s offset %s' % (
        300, int(pp) * 300)
    a = MySQLHelper()
    NovelUrl = a.SqlFecthAll(sql)
    a.CloseCon()

    proxies = fetchproxies(40)
    for i in NovelUrl:
        try:
            header = get_header()
            proxy = random.choice(proxies)
            print i[0]
            CrawlNovelData(i[0], header, proxy)
        except Exception as e:
            print 'error'
            print e.message
            pass


def Main(url):
    Main_CrawlNovelList(url, 200)
    threads = []
    for i in range(60):
        t1 = threading.Thread(target=Main_CrawlNovel, args=(i,))
        threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

    threads = []
    for i in range(60):
        t1 = threading.Thread(target=Main_CrawlNovelData, args=(i,))
        threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()
    print time.ctime()


if __name__ == '__main__':
    url = r'http://www.yousuu.com/booklist'
    Main(url)
