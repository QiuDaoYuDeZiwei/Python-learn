# coding= utf-8

import sys, shutil, os, string
import re
import time

#shutil  offers a number of high-level operations on files and collections of files.
#https://docs.python.org/2/library/shutil.html

pathlist =  [r'D:\WORK', r'D:\BaiduNetdiskDownload' r'C:\Users\92114\Desktop'] # 不全的path

def BFS_Dir(path, dirCallback = None, fileCallback = None):
    queue = []
    ret = []
    queue.append(path);
    while len(queue) > 0:
        tmp = queue.pop(0)
        if(os.path.isdir(tmp)):
            #ret.append(tmp)
            for item in os.listdir(tmp):
                queue.append(os.path.join(tmp, item))
            if dirCallback:
                dirCallback(tmp)
        elif(os.path.isfile(tmp)):
            ret.append(tmp)
            if fileCallback:
                fileCallback(tmp)
    return ret

def DFS_Dir(path, dirCallback = None, fileCallback = None):
    stack = []
    ret = []
    stack.append(path);
    while len(stack) > 0:
        tmp = stack.pop(len(stack) - 1)
        if(os.path.isdir(tmp)):
            #ret.append(tmp)
            for item in os.listdir(tmp):
                stack.append(os.path.join(tmp, item))
            if dirCallback:
                dirCallback(tmp)
        elif(os.path.isfile(tmp)):
            ret.append(tmp)
            if fileCallback:
                fileCallback(tmp)
    return ret

def printDir(path):
    print "dir: " + path

def printFile(path):
    print "file: " + path

def cpFile(destDir, srcPath):
    fileName = os.path.basename(srcPath)
    destPath = destDir  + os.path.sep + fileName  # os.path.sep : \\
    if os.path.exists(srcPath) and not os.path.exists(destPath):
        print 'cp %s %s' % (srcPath,destPath)
        shutil.copy(srcPath,destPath)
        return(str('cp %s --> %s' % (srcPath,destPath)))
    else:
        return('Nothing to Copy')

def MacthCopy(item):
    u"""
    寻找pdf, sql, py , R的文件,并复制到相应的文件夹下,写入日志.
    """
    copylog = open(r'D:\code_programming\Log\CopyLog.log', 'a+')
    if re.match(r'.*python.*pdf$|.*sql.*pdf$|.*program.*pdf$|.*rlanguage-.*pdf$', item.lower()):
        writetmp = cpFile(r'D:\PDF', string.strip(item))
        if writetmp !=  'Nothing to Copy':
            copylog.write(str(time.ctime( ))+'  '+ writetmp +'\n')
    if re.match(r'.*\.r$', item.lower()):
        writetmp =  cpFile(r'D:\code_programming\rcode', string.strip(item))
        if writetmp !=  'Nothing to Copy':
            copylog.write(str(time.ctime( ))+'  '+ writetmp +'\n')
    if re.match(r'.*\.py$', item.lower()):
        writetmp = cpFile(r'D:\code_programming\pythoncode', string.strip(item))
        if  writetmp !=  'Nothing to Copy':
            copylog.write(str(time.ctime( ))+'  '+ writetmp +'\n')
    if re.match(r'.*\.sql$', item.lower()):
        writetmp = cpFile(r'D:\code_programming\sqlcode', string.strip(item))
        if writetmp !=  'Nothing to Copy':
            copylog.write(str(time.ctime( ))+'  '+ writetmp +'\n')
    if re.match(r'.*\.whl$', item.lower()):
        writetmp = cpFile(r'D:\python_packages', string.strip(item))
        if  writetmp !=  'Nothing to Copy':
            copylog.write(str(time.ctime( ))+'  '+ writetmp +'\n')
    copylog.close()

if __name__ == '__main__':
    for path in pathlist:
        b = BFS_Dir(path)
        #d = DFS_Dir(path, printDir, printFile)
        for item in b:
            MacthCopy(item)
    copylog = open(r'D:\code_programming\Log\CopyLog.log', 'a+')
    copylog.write(str(time.ctime( ))+'  Running' +'\n')
    copylog.close()
