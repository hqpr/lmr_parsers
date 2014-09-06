# -*- coding: cp1251 -*-


import csv
import urllib
import time
import re
import MySQLdb
import lxml.html
import httplib

# .decode('cp1251').encode('utf-8')

url = 'page.htm'
c = urllib.urlopen(url)
data = c.read()
match = re.findall('itemprop\=\"name\".style\=\"text-align\:center\;\"[>](.*)[<]\/h1[>]', data)
print match[0].decode('cp1251').encode('utf-8')

