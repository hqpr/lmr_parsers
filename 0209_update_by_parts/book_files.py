#! /usr/bin/env python
# -*- coding: cp1251 -*-

"""
Сбор файлов epub, mobi, txt, html

Работает для тех, у кого есть источник и нет значения в колонке txtlink
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

sleep = 1

# Для рабочей машины вручную прописал путь
path = 'C:/Users/user/Dropbox/Public/letmeread/parsers/2014'

result = {}


def parser():
    cur.execute("SELECT * FROM page_book")
    for row in cur.fetchall():
        book_source = row[5]
        if not row[13]:
            if book_source and book_source != '1':
                book_id = row[0]
                url_id = re.findall(r'\=(\d+)', book_source)
                url_id = url_id[0]
                if not book_id in result:
                    result.update({book_id: []})

                time.sleep(sleep)
                html = lxml.html.parse(book_source)
                print
                print '%s [%s] => %s' % (row[0], row[1], book_source)
                try:
                    rating = html.xpath('//span/span[2]/span[1]/text()')[0]
                    result[book_id].append(rating)
                except IndexError:
                    try:
                        rating = html.xpath('//span[2]/span[1]/text()')[0]
                        result[book_id].append(rating)
                    except IndexError:
                        try:
                            rating = html.xpath('//td[2]/span/span[2]/span[1]/text()')[0]
                            result[book_id].append(rating)
                        except IndexError:
                            pass
                except:
                    pass
                time.sleep(sleep)
                c = urllib.urlopen(book_source)

                match = re.findall(r'\"epub.php\/\d+\/(.*).epub\"|\"txt.php\/\d+\/(.*).txt\"|\"mobi.php\/\d+\/(.*).mobi\"|\"bookreader.php\/save\/\d+\/(.*).html\"|itemprop\=\"description\"[>](.*)[<]\/span', c.read())

                for m in match:
                    if m[0]:
                        epub = 'http://www.e-reading.me/epub.php/%s/%s.epub' % (url_id, m[0])
                        urllib.urlretrieve(epub, '%s/epub/%s.epub' % (path, book_id))
                    if m[1]:
                        txt = 'http://www.e-reading.me/txt.php/%s/%s.txt' % (url_id, m[1])
                        urllib.urlretrieve(txt, '%s/txt/%s.txt' % (path ,book_id))
                    if m[2]:
                        mobi = 'http://www.e-reading.me/mobi.php/%s/%s.mobi' % (url_id, m[2])
                        urllib.urlretrieve(mobi, '%s/mobi/%s.mobi' % (path, book_id))
                    if m[3]:
                        html = 'http://www.e-reading.me/bookreader.php/save/%s/%s.html' % (url_id, m[3])
                        urllib.urlretrieve(html, '%s/html/%s.html' % (path, book_id))
                break


def db_updater(main_dict):
    for k, v in result.items():
        # epub = 'download/epub/%s.epub' % k
        epub = 'http://lmr.url.ph/d/epub/%s.epub' % k
        if not epub:
            epub = None
        # txt = 'download/txt/%s.txt' % k
        txt = 'http://lmr.url.ph/d/txt/%s.txt' % k
        if not txt:
            txt = None
        # mobi = 'download/mobi/%s.mobi' % k
        mobi = 'http://lmr.url.ph/d/mobi/%s.mobi' % k
        if not mobi:
            mobi = None

        html = 'download/html/%s.html' % k
        sql = "UPDATE page_book SET txtlink = '%s', htmllink = '%s', mobilink = '%s', epublink = '%s' WHERE id = '%s'" % (txt, html, mobi, epub, k)
        try:
            cur.execute(sql)
            db.commit()
            print '[OK] %s Saved' % k
            result.clear()
        except:
            db.rollback()
            print '%s [error]' % k

cur.execute("SELECT id, name, source, txtlink FROM page_book")
for row in cur.fetchall():
    if not row[3]:
        parser()
        db_updater(result)
        # continue

