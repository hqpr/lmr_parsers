#! /usr/bin/env python
# -*- coding: cp1251 -*-

"""
Собирает картинку к книге, если нет
Смотрит в поле source
работает все, заебись
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
sleep = 2

result = {}

DOMAIN = 'http://www.e-reading.me'


def parser():
    book_source = row[2]
    if book_source and book_source != '1':
        book_id = row[0]
        time.sleep(sleep)
        c = urllib.urlopen(book_source)

        # print c.read()

        match = re.findall('img.src\=\"(.*)\".alt', c.read())
        if match[0] == '/images/cover.jpg':
            picture = None
        else:
            picture = '%s%s' % (DOMAIN, match[0])
            try:
                urllib.urlretrieve(picture, 'jpg/%s.jpg' % book_id)
                img = 'img/book/%s.jpg' % book_id
                sql = "UPDATE page_book SET image = '%s' WHERE id = '%s'" % (img, book_id)
                try:
                    cur.execute(sql)
                    db.commit()
                    print '> [%s] =>  %s' % (book_id, picture)
                except:
                    db.rollback()
                    print '%s [error]' % book_id
            except:
                print '-- [%s] => Not found' % book_id

cur.execute("SELECT id, image, source FROM page_book where image is null")
for row in cur.fetchall():
    image = row[1]
    if not image:
        parser()


