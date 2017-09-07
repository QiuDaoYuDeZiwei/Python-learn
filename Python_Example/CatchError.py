#coding= utf-8

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


class WupeiqiException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


try:
    raise WupeiqiException('我的异常')
except WupeiqiException, e:
    print e.message.decode('utf-8')
    # env windows print e.message  乱码
    # env linux print  e.message.decode('utf-8') 乱码
print 'ok'
