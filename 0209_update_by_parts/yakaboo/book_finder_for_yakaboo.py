#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

db_books = {}
cur.execute("SELECT id, `name` FROM page_book")
for row in cur.fetchall():
    db_books.update({row[0]: row[1]})  # ID: NAME

csv_d = {}
reader = csv.reader(open('ozon.csv', 'rb'), delimiter=';', quotechar='"')
for row in reader:
    name = row[0].decode('cp1251')
    if name in db_books.values():
        csv_d.update({name: [row[1], row[2]]})  # NAME: URL, PRICE

result = {}
for k, v in db_books.items():
    for p, z in csv_d.items():
        if v in p:
            result.update({k: [z[0], z[1]]})

for a, b in result.items():
    sql = "UPDATE page_book SET yakaboo = '%s', yakaboo_price = '%s' WHERE id = '%s'" % (b[0], b[1], a)
    try:
        cur.execute(sql)
        db.commit()
        print '[OK] %s Saved' % a
        result.clear()
    except:
        db.rollback()
        print '%s [error]' % a

