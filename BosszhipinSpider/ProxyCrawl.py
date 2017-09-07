#coding= utf-8
__author__ = 'syy'

u"""
crawl number:count proxies
"""

import time, random, traceback
import requests
from bs4 import  BeautifulSoup
from config import TIMEOUT, get_header, CrawlProxy_URL
from TestProxies import TestProxy

def ProxiesGet(count):
    u"""
    crawl number:count useful proxies
    return a list --proxies
    """
    proxies = []
    try:
        header = get_header()
        for i in xrange(1,10):
            for url in CrawlProxy_URL:
                url = url + str(i)
                if not proxies:
                    res = requests.get(url,headers=header,timeout = TIMEOUT).text
                else:
                    proxy = random.choice(proxies)
                    res = requests.get(url,headers=header,proxies=proxy, timeout = TIMEOUT).text
                soup = BeautifulSoup(res)
                ips = soup.findAll('tr')

                for x in range(1,len(ips)): #ips[0] 是列标题 国家 IP地址 端口 类型http https： tds[5].contents[0].lower()
                    ip = ips[x]
                    tds = ip.findAll("td")
                    ip_temp = tds[1].contents[0]+"\t"+tds[2].contents[0]+"\n"
                    if tds[5].contents[0].lower() == u'http':
                        ip = ip_temp.strip("\n").split("\t")
                        proxy_host = "http://"+ip[0]+":"+ip[1]
                        proxy_temp = {"http":proxy_host}
                        if TestProxy(proxy_temp):
                            proxies.append(proxy_temp)
                    if len(proxies) >= count:
                        return proxies
    except Exception as e:
        #traceback.print_exc()
        #traceback.print_exc(file=open(r'./ProxiesGet_Error.log','a+'))
        pass
