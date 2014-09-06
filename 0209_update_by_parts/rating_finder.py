#! /usr/bin/env python
# -*- coding: cp1251 -*-

import csv
import urllib
import time
import re
import MySQLdb
import lxml.html
import httplib

db = MySQLdb.connect(host="127.0.0.1",
# db = MySQLdb.connect(host="194.54.81.222",
user="letmerea_alex",
passwd="dbpassword451xQkk",
db="letmerea_book",
charset='utf8')

SLEEP = 3

cur = db.cursor()
cur.execute("SELECT id, source FROM page_book WHERE source is not null and source <> '1' and rating is null")
for row in cur.fetchall():
    book_id = row[0]
    source = row[1]
    c = urllib.urlopen(source)
    data = c.read()
    rating = re.findall('itemprop\=\"average\"[>](...)[<]\/span[>]', data)
    if rating:
        sql = "UPDATE page_book SET rating='%s' WHERE id = '%s'" % (rating[0], book_id)
        try:
            cur.execute(sql)
            db.commit()
            print '[OK] %s = %s' % (book_id, rating[0])
        except:
            db.rollback()
            print '[ERROR] %s' % book_id
            pass
        time.sleep(SLEEP)



        #
        # # print book_source
        #
        # time.sleep(SLEEP)
        #
        # c = urllib.urlopen(book_source)
        # data = c.read()
        # match = re.findall('itemprop\=\"name\".style\=\"text-align\:center\;\"[>](.*)[<]\/h1[>]', data)
        # book_name = match[0].decode('cp1251').encode('utf-8')
        #
        # sql = "INSERT INTO page_book (author_id, `name`, source) values ('%s','%s','%s')" % (author_id, book_name, book_source)
        # try:
        #     cur.execute(sql)
        #     db.commit()
        # except:
        #     pass
        # print '[OK] %s += %s' % (author_id, book_name)
        # print
        # # break






