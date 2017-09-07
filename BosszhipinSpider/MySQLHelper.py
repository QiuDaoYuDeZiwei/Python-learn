#coding= utf-8
__author__ = 'syy'

u"""
MYSQLHelper
"""

import MySQLdb
from config import DB_CONFIG


class MYSQLHelper(object):
    u"""class MYSQLHelper.
    SqlExecute,SqlFecthAll,CloseCon
    config.py
    """

    def __init__(self):
        self.con = MySQLdb.connect(DB_CONFIG['host'], DB_CONFIG['use'], DB_CONFIG['password'],
                                   DB_CONFIG['database'], charset=DB_CONFIG['charset'])
        self.cursor = self.con.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.con.commit()

    def SqlExecute(self, sql):
        self.cursor.execute(sql)
        self.con.commit()

    def SqlFecthAll(self, sql):
        """return a tuple"""
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def CloseCon(self):
        self.con.close()
