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

DOMAIN = 'http://www.e-reading.me'
SLEEP = 2

new_book = {}
cur = db.cursor()
cur.execute("SELECT id, source FROM page_author WHERE source is not null and id >= 373")
for row in cur.fetchall():
    author_id = row[0]
    source = row[1]
    c = urllib.urlopen(source)
    data = c.read()
    urls = re.findall('a.href\=\"(\/book.php\?book\=\d+)\".title\=\".*\"[>].*[<]\/a[>]', data)
    for u in urls:
        book_source = '%s%s' % (DOMAIN, u)
        # print book_source

        time.sleep(SLEEP)

        c = urllib.urlopen(book_source)
        data = c.read()
        match = re.findall('itemprop\=\"name\".style\=\"text-align\:center\;\"[>](.*)[<]\/h1[>]', data)
        book_name = match[0].decode('cp1251').encode('utf-8')

        sql = "INSERT INTO page_book (author_id, `name`, source) values ('%s','%s','%s')" % (author_id, book_name, book_source)
        try:
            cur.execute(sql)
            db.commit()
        except:
            pass
        print '[OK] %s += %s' % (author_id, book_name)
        print
        # break

    # for k, v in new_book.items():
    #     sql = "INSERT INTO page_book (author_id, `name`, source) values ('%s','%s','%s')" % (k, v[0], v[1])
    #     cur.execute(sql)
    #     db.commit()
    #     print '[OK] %s, %s' % (v[0], v[1])

        # continue


