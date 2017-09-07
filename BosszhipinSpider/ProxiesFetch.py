#coding= utf-8
__author__ = 'syy'

import traceback
from SaveData import TABLEipHelper
from ProxyCrawl import ProxiesGet
from TestProxies import TestProxy

def FetchProxies():
    u"""
    从MySQL表ip fetch
    return a list —— proxies
    """
    try:
        c = TABLEipHelper()
        c.CreateTableIP()
        sql = 'select ip from ip'
        results = c.SqlFecthAll(sql)
        c.CloseCon()
        proxies = []
        for i in results: # i is a tuple ('http://218.106.98.166:53281',)
            proxy_host = i[0]
            proxy_temp = {"http":proxy_host}
            proxies.append(proxy_temp)
        return proxies
    except Exception as e:
        #traceback.print_exc(file=open(r'./FetchProxies_Error.log','a+'))
        return []

def HaveProxies(count):
    u'''
    fetch table ip
    TestProxy : test ip
    if ip > count,return useful proxies
    else
    ProxiesGet,Save proxies,FetchProxies
    return useful proxies
    '''
    UseFulproxies = []
    try:
        proxies = FetchProxies()
        for proxy in proxies:
            if TestProxy(proxy):
                UseFulproxies.append(proxy)
            if len(UseFulproxies) >= count:
                return UseFulproxies
        print 'TABLE ip has not enough proxies'

        proxies = ProxiesGet(count)
        c = TABLEipHelper()
        c.TruncTableIP()
        for  proxy in proxies:
            c.InsertIP(proxy)
        c.CloseCon()
        return proxies
    except Exception as e:
        #traceback.print_exc(file=open(r'./HaveProxies_Error.log','a+'))
        pass
