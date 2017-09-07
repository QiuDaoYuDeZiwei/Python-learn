#conding= utf-8
__author__ = 'syy'

u'''
这是《core python 核心编程》的练习答案.
'''
# 1.1
p = re.compile(r'.*(bat|bit|but|hat|hit|hut)$')
# 1.2 单词对
p = re.compile(r'^\w+\s\w+$')
# 1.3
p = re.compile(r'(\w+[\s,])*\w+$')
# 1.4
#import keyword
# keyword.kwlist
p = re.compile(r'^[a-zA-Z_][\w_]*$')
# 1.5
p = re.compile(r'^\d{4}\s(\S*\s)*\S*$')
# 1.6
p = re.compile(r'^www://www\.(\S*\.)*com$')
p = re.compile(r'^(www|http)://www\.(\S*\.)*(com|edu|net)$')
# 1.7
#import sys
# sys.maxint ##2147483647
p = re.compile(
    r'(^[01]\d{0,9}$)|(^2[01][0-4][0-7][0-4][0-8][0-3][0-6][0-4][0-7]$)')
#1.8
p=re.compile(r'^\d*L$')
#1.9
p=re.compile(r'^\d*\.\d*')
#1.10
p=re.compile(r'(\(\d*+\d*j\))|(\d*j)')
