# -*- coding: utf-8 -*-

u"""
改自徐璐发的python3的版本
modified：
1.版本为python2.7
2.结果写入Mysql数据库
"""
print __doc__

import time
import random
import re
import sys
import threading
# Excel写入库 import xlwt  python3
import MySQLdb
import requests
from bs4 import BeautifulSoup

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

sys.path.append(r'D:\GitHub\python')
from GetProxy import *

# 链家网页爬虫：http://www.tuicool.com/articles/zMrUryb


def buildInfoList(pageCount):
    url_page = 'http://nj.lianjia.com/xiaoqu/'
    listResult = []
    # 目前链家网该链接只能提供100个页面进行爬取
    try:
        # 拼接URL
        currentUrl = url_page
        if pageCount != 0:
            currentUrl = url_page + 'pg' + str(pageCount) + '/'
        print(currentUrl)
        # 形成代理IP

        header = BuildHds()
        proxy = GetUseProxy(proxies)

        # 请求服务器
        source_code = requests.get(currentUrl, headers=header, proxies=proxy)
        soup = BeautifulSoup(source_code.text)
        # print soup
        xiaoqu_list = soup.findAll('li', {'class': 'clear xiaoquListItem'})
        # 解析URL
        for xq in xiaoqu_list:
            # print(xp)
            info_dict = {}
            info_dict.update(
                {u'小区名称': xq.find('div', {'class': 'title'}).find('a').text})
            info_dict.update(
                {u'90天成交量': xq.find('div', {'class': 'houseInfo'}).find('a').text})
            positionInfo = xq.find('div', {'class': 'positionInfo'})
            info_dict.update({u'所在区': positionInfo.findAll('a')[0].text})
            info_dict.update({u'所在板块': positionInfo.findAll('a')[1].text})
            buildYear = re.search(ur"\d\d\d\d年建成", positionInfo.text)
            if buildYear:
                buildYear = buildYear.group()
                info_dict.update({u'建成时间': buildYear})
            else:
                info_dict.update({u'建成时间': 'NULL'})
            info_dict.update(
                {u'小区均价': xq.find('div', {'class': 'totalPrice'}).find('span').text})
            info_dict.update({u'在售套数': xq.find(
                'div', {'class': 'xiaoquListItemSellCount'}).find('span').text})
            if any(info_dict):
                listResult.append(info_dict)
                # print(info_dict)
        return listResult
    except Exception as e:
        print e
        return []


# 将记录有结果的Table对象存储到mysql
def Savemysql(listResult):
    try:
        nrows = len(listResult)
        c = IPMySQL()
        sql = """CREATE TABLE IF NOT EXISTS  lianjia (
                 date datetime,
                 communityname text,
                 amount90 text ,
                 county  text,
                 plate text,
                 builddate  text,
                 averageprice text,
                 numberofsolds text )
                 DEFAULT CHARSET=utf8"""
        c.SqlExecute(sql)

        for rowi in range(1, nrows):
            sql = """insert into lianjia values ('%s','%s' ,'%s','%s','%s','%s','%s','%s') """ \
                % (time.strftime('%Y-%m-%d %X', time.localtime(time.time())), listResult[rowi][u'小区名称'], listResult[rowi][u'90天成交量'], listResult[rowi][u'所在区'],
                   listResult[rowi][u'所在板块'], listResult[rowi][u'建成时间'], listResult[rowi][u'小区均价'], listResult[rowi][u'在售套数'])
            print sql
            c.SqlExecute(sql)
        c.CloseCon()
    except Exception as e:
        print e


if __name__ == "__main__":
    proxies = HiveProxys(5)
    for i in xrange(1, 101):
        infoList = buildInfoList(i)
        if len(infoList):
            Savemysql(infoList)
    print str(time.strftime('%Y-%m-%d %X', time.localtime(time.time()))) + ' ok'
