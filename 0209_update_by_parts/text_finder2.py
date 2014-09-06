#! /usr/bin/env python
# -*- coding: cp1251 -*-

"""
Собирает текс к книге, если нет
Смотрит в поле source


Частично работает
"""


import csv
import urllib
import time
import re
import MySQLdb
import lxml.html


# db = MySQLdb.connect(host="194.54.81.222",
db = MySQLdb.connect(host="127.0.0.1",
user="letmerea_alex",
passwd="dbpassword451xQkk",
db="letmerea_book",
charset='utf8')

cur = db.cursor()

SLEEP = 2
cur.execute("SELECT id, text, source FROM page_book")
for row in cur.fetchall():
    text = row[1]
    if not text:
        book_source = row[2]
        if book_source and book_source != '1':
            book_id = row[0]
            time.sleep(SLEEP)
            c = urllib.urlopen(book_source)

            # print c.read()

            match = re.findall('itemprop\=\"description\">(.*)<\/span>', c.read())
            if match:
                if match[0]:
                    result = match[0].decode('cp1251').encode("utf-8")
                    # result = match[0].decode('utf-8')
                    # result = unicode(match[0], errors='ignore')
                    result = result.replace('\n', '').replace('\r\n', '').replace('<br />', '')
                    try:
                        sql = "UPDATE page_book SET text = '%s' WHERE id = '%s'" % (result, row[0])
                        cur.execute(sql)
                        db.commit()
                        print '[OK] %s: %s' % (result, row[0])
                        print
                    except:
                        sql = "UPDATE page_book SET text = '1' WHERE id = '%s'" % row[0]
                        cur.execute(sql)
                        db.commit()
                        print '[ERROR] %s' % row[0]
                        print

            else:
                sql = "UPDATE page_book SET text = '1' WHERE id = '%s'" % row[0]
                cur.execute(sql)
                db.commit()
                print 'Nothing on %s -> %s' % (book_id, row[2])
                print

# for k, v in d.items():
#     try:
#         sql = "UPDATE page_book SET text = '%s' WHERE id = '%s'" % (v, k)
#         cur.execute(sql)
#         db.commit()
#         print '[OK] %s: %s' % (k, v)
#         d.clear()
#     except:
#         sql = "UPDATE page_book SET text = '1' WHERE id = '%s'" % row[0]
#         cur.execute(sql)
#         db.commit()
#         print '[ERROR] %s' % k


    # continue







