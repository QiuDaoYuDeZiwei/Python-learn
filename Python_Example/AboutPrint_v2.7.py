#coding= utf-8
__author__ = 'syy'


u"""
Python version : 2.7

Description : print 支持输出重定向到文件
"""

import os
import sys
f=open(r'D:/test.txt','w+')
print >> f,'test'
f.close()
print >> sys.stderr ,'test'
os.remove(r'D:/test.txt')