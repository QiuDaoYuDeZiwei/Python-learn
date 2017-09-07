#coding= utf-8
__author__ = 'syy'

import time
import chardet  # chardet是一个非常优秀的编码识别模块
import requests
from config import TEST_IP, TEST_URL, TIMEOUT, get_header
import json

def getMyIP():
    try:
        r = requests.get(url=TEST_IP, headers=get_header(), timeout=TIMEOUT)
        ip = json.loads(r.text)
        return ip['origin']
    except Exception as e:
        print e.message


def TestProxy(proxy):
    u"""TestProxy
    test config.TEST_URL
    proxy is a dict
    proxy ok , return proxy
    """
    try:
        r = requests.get(url=TEST_URL, headers=get_header(),
                         timeout=TIMEOUT, proxies=proxy)
        r.encoding = chardet.detect(r.content)['encoding']
        if r.ok:
            print proxy
            return proxy
        else:
            print time.strftime('%Y-%m-%d %X', time.localtime(time.time())) + ' uselessful ip ', proxy
            return None
    except Exception as e:
        print time.strftime('%Y-%m-%d %X', time.localtime(time.time())) + ' uselessful ip ', proxy
        return None


def baidu_check(proxy):
    u'''
    用百度来测试
    '''
    try:
        r = requests.get(url='https://www.baidu.com',
                         headers=get_header(), timeout=TIMEOUT, proxies=proxy)
        r.encoding = chardet.detect(r.content)['encoding']
        if r.ok:
            print proxy
            return proxy
        else:
            print time.strftime('%Y-%m-%d %X', time.localtime(time.time())) + ' uselessful ip ', proxy
            return None
    except Exception as e:
        print time.strftime('%Y-%m-%d %X', time.localtime(time.time())) + ' uselessful ip ', proxy
        return None
a = 1