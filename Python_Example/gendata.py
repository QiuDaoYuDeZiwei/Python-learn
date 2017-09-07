#conding= utf-8

u'''
该脚本为正则表达式创建随机数据，然后将生成的数据输出到屏幕。
要将该程序移植到Python3，仅需要将print语句修改为函数，将xrange()修改为range(),
以及将sys.maxint 修改为sys.maxsize.
'''

from random import randrange, choice
from string import ascii_lowercase as lc
from sys import maxint
from time import ctime

tlds = ('com', 'edu', 'net', 'org', 'gov')

for i in xrange(randrange(5, 11)):
    dtint = randrange(maxint)
    dtstr = ctime(dtint)
    llen = randrange(4, 8)
    login = ''.join(choice(lc))
    dlen = randrange(llen, 13)
    dom = ''.join(choice(lc) for j in xrange(dlen))
    print '%s::%s@%s.%s::%d-%d-%d' % (dtstr, login, dom, choice(tlds), dtint, llen, dlen)
