#! /usr/bin/env python
# -*- coding: cp1251 -*-

"""
изменение адреса файла с локального хоста - на доп хостинг
"""


import csv
import urllib
import time
import re
import MySQLdb
import lxml.html

db = MySQLdb.connect(host="127.0.0.1",
user="letmerea_alex",
passwd="dbpassword451xQkk",
db="letmerea_book",
charset='utf8')
cur = db.cursor()

cur.execute("SELECT id, txtlink FROM page_book where txtlink is not null")
for row in cur.fetchall():
    if 'http' not in row[1]:
        new_path = 'http://lmr.url.ph/d/txt/%s.txt' % row[0]
        # print new_path
        sql = "UPDATE page_book SET txtlink = '%s' WHERE id = '%s'" % (new_path, row[0])
        try:
            cur.execute(sql)
            db.commit()
            print '> [%s] =>  %s' % (row[0], new_path)
        except:
            db.rollback()
            print '%s [error]' % row[0]