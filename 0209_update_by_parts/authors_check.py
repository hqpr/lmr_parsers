#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Проверка на соответсвие автора=книга

Смотрим автора на сайте е-ридинг
если авторы совпадают - обновляю стобец link в таблице page_book на 1
и обноляю ссылку на еридинг в таблицу page_author
"""


import csv
import urllib
import time
import re
import MySQLdb
import lxml.html
import httplib

SLEEP = 2

db = MySQLdb.connect(host="127.0.0.1",
# db = MySQLdb.connect(host="194.54.81.222",
user="letmerea_alex",
passwd="dbpassword451xQkk",
db="letmerea_book",
charset='utf8')

cur = db.cursor()

cur.execute("SELECT id, name, author_id, source, link FROM page_book WHERE source <> '1'")
for row in cur.fetchall():
    if not row[4]:
        book_id = row[0]
        author_id = row[2]
        print row[3]
        print '- %s - ' % row[1]
        c = urllib.urlopen(row[3])
        data = c.read()
        new_name = re.findall('bookbyauthor.php\?author=\d+\".title\=\"(.*)\"[>][<]', data)
        found_some = new_name[0].decode('cp1251').encode('utf-8')
        found_some = found_some.split(' ')
        found_some = '%s %s' % (found_some[-1], found_some[0])
        print found_some

        new_source = re.findall('(bookbyauthor.php\?author=\d+)\".title\=\".*\"[>][<]', data)
        source = 'http://www.e-reading.me/%s' % new_source[0]

        print '='

        cur.execute("SELECT id, name FROM page_author where id = %s" % author_id)
        for row in cur.fetchall():
            author_name = row[1]
            a_name = author_name
            print author_name

        x = raw_input('> Correct? ')
        if x == 'n':
            cur = db.cursor()
            try:
                found_some = found_some.decode('utf-16').encode('utf-16').decode('cp1251').encode('utf-8')
                found_some = found_some[4:]
            except:
                pass
            sql = "SELECT page_author.`name` FROM `page_author` WHERE page_author.`name` LIKE '%s'" % found_some
            if cur.execute(sql) == 1:
                cur.execute("SELECT id, name FROM page_author WHERE name LIKE '%s'" % found_some)
                for row in cur.fetchall():
                    print u'Найдено в базе %s' % row[1]
                    x = raw_input('> Update Author to new? ')
                    if x == 'y':
                        sql = "UPDATE page_book SET author_id = '%s' WHERE id = '%s'" % (row[0], book_id)
                        cur.execute(sql)
                        db.commit()
                        print '[OK] Authors ID updated'
                        print
                    else:
                        break
            else:
                print u'Автор не найден'
                print
                continue

        else:
            sql = "UPDATE page_book SET link = '1' WHERE id = '%s'" % book_id
            cur.execute(sql)
            db.commit()

            sql = "UPDATE page_author SET source = '%s' WHERE id = '%s'" % (source, author_id)
            cur.execute(sql)
            db.commit()
            # print '[OK] updated!'

        print










    #     sql = "UPDATE page_book SET source = '%s' WHERE id = '%s'" % (new_url, row[0])
    #     try:
    #         cur.execute(sql)
    #         db.commit()
    #         # time.sleep(SLEEP)
    #         print '[OK] %s -> %s (%s)' % (row[0], new_url, row[1])
    #         print
    #         # continue
    #     except:
    #         db.rollback()
    #         print '[error in db query]'
    # else:
    #     sql = "UPDATE page_book SET source = '1' WHERE id = '%s'" % row[0]
    #     print
    #     try:
    #         cur.execute(sql)
    #         db.commit()
    #     except:
    #         db.rollback()
    #         print '[error in db query]'
    time.sleep(SLEEP)
