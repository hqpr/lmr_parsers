#! /usr/bin/env python
# -*- coding: cp1251 -*-

"""
Обновляем ИСТОЧНИК книги, у которых не заполнены поля
Ручное управление при добавдение книги

Ищет название на сайте e-reading, принтит в консоль.

Чтобы записать в базу источник - нажать 'y'

"""


import csv
import urllib
import time
import re
import MySQLdb
import lxml.html
import httplib

SLEEP = 1

db = MySQLdb.connect(host="127.0.0.1",
# db = MySQLdb.connect(host="194.54.81.222",
user="letmerea_alex",
passwd="dbpassword451xQkk",
db="letmerea_book",
charset='utf8')

cur = db.cursor()

cur.execute("SELECT * FROM page_book")
""" Апдейтер в базу. Если книга не соответсвует найденному на сайте
        е-ридинг - книге в столбцец source проставляется 1 (как ошибка)."""
for row in cur.fetchall():
    txt = row[13]
    book_name = row[1]
    source = row[5]
    book_name = book_name.encode('cp1251')
    if not source and source != '1':
        conn = httplib.HTTPConnection("www.e-reading.me")
        f = {'query': '%s' % book_name}
        conn.request("GET", "/?%s" % urllib.urlencode(f))
        res = conn.getresponse()
        if res.status != 200:
            raise Exception("Connection Error!")
        data = res.read()

        match = re.findall(r'book.php\?book=(\d+)\&', data)
        if match:
            new_url = 'http://www.e-reading.me/book.php?book=%s' % match[0]

            c = urllib.urlopen(new_url)
            new_name = re.findall('h1.itemprop\=\"name\".*\"[>](.*)[<]\/h1', c.read())
            found_some = new_name[0].decode('cp1251').encode('utf-8')

            print row[1]
            print '||'
            print found_some

            x = raw_input('> Update? ')
            if x == 'y':
                sql = "UPDATE page_book SET source = '%s' WHERE id = '%s'" % (new_url, row[0])
                try:
                    cur.execute(sql)
                    db.commit()
                    # time.sleep(SLEEP)
                    print '[OK] %s -> %s (%s)' % (row[0], new_url, row[1])
                    print
                    # continue
                except:
                    db.rollback()
                    print '[error in db query]'
            else:
                sql = "UPDATE page_book SET source = '1' WHERE id = '%s'" % row[0]
                print
                try:
                    cur.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                    print '[error in db query]'
        # time.sleep(SLEEP)
