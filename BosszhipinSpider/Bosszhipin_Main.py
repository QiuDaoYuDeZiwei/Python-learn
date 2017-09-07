#coding= utf-8
__author__ = 'syy'

u"""
env: windows
author: syy
target: crawl boss直聘 杭州数据分析 的前25页
tips: 不采用正则的做法,而是采用bs4的BeautifulSoup.使用了代理ip和header。
"""
# 需要写 u 否则 print __doc__ 是乱码
print __doc__

import sys
import random
import time
import traceback
from BossZhipinCrawl import html_Download
from ProxiesFetch import HaveProxies

# 修改编码 utf-8
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    try:
        proxies = HaveProxies(50)
        for i in xrange(1, 26):
            proxy = random.choice(proxies)
            html_Download(proxy, i)
        print str(time.strftime('%Y-%m-%d %X', time.localtime(time.time()))) + ' ok'
    except Exception, e:
        traceback.print_exc(file=open(r'./BossZhiPin_Error.log', 'w+'))
