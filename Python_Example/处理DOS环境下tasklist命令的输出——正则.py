#conding= utf-8

u"""
这里的脚本使用一个正则表达式和findall()解析DOS环境下tasklist命令的输出
但是仅仅显示感兴趣的数据.将改脚本移植到python3 ，仅仅需要修改print()函数
"""
import os
import re
f= os.popen('tasklist /nh','r')
p = re.compile(r'([\w.]+(?: [\w.]+)*)\s\s+(\d+) \w+\s\s+\d+\s\s+([\d,]+ K)')
for eachLine in f:
    print re.findall(p, eachLine.rstrip())
f.close()