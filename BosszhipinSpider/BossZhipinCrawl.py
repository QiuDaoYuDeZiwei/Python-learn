#coding= utf-8
__author__ = 'syy'

u"""
crawl boss直聘 杭州数据分析 的前25页
tips: 采用bs4的BeautifulSoup.使用了代理ip和header。
"""

import re, time, random
import MySQLdb
import requests
from bs4 import BeautifulSoup
from SaveData import TABLEzhipinHelper
from config import get_header

def html_Download(proxy,page):
    u"""
    爬数据 写入mysql.
    爬一次，sleep 1s。
    """
    url = "https://www.zhipin.com/c101210100/h_101210100/?query=%%E6%%95%%B0%%E6%%8D%%AE%%E5%%88%%86%%E6%%9E%%90&page=%s&ka=page-%s"\
            %(page, page )  # %s  %% 百分号
    p =  re.compile(r'\n+| +', re.S)
    Findjob_detail_url = re.compile(r'href="/job_detail/(.*?)" ka', re.S)
    try:
        c = TABLEzhipinHelper()
        c.CreateTablezhipin()
        headers = get_header()

        source_code = requests.get(url, headers = headers, proxies = proxy)
        soup = BeautifulSoup(source_code.text)
        job_list = soup.findAll('div', 'job-primary')
        for job in job_list:
            detail = re.split(',', re.sub(p, ',', job.text.strip()))
            detail_url = 'https://www.zhipin.com/job_detail/' + re.findall(Findjob_detail_url,str(job))[0]
            detail.append(detail_url)
            c.Insertzhipin(detail)
        print 'page %s is done at %s' % (page, time.ctime())
        c.CloseCon()
        #time.sleep(1)
    except Exception as e:
        #traceback.print_exc(file = open(r'./html_Download_Error.log','a+'))
        print e
        pass
    