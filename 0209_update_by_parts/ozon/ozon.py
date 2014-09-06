import xml.etree.cElementTree as etree
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Data"
def write(col, row, sheet, data):
    while True:
        try:
            sheet['%s%s' %(col,row)] = data
            break
        except:
            try:
                sheet['%s%s' %(col,row)] = " ".join(data)
                break
            except:
                try:
                    d2 = []
                    for i in data:
                        d2.append(" ".join(i))
                    sheet['%s%s' %(col,row)]= " ".join(d2)
                    break
                except:
                    sheet['%s%s' %(col,row)]= " "
                    break

r = 1
write('A', r, ws, "TITLE")
write('B', r, ws, "URL")
write('C', r, ws, "PRICE")

wb.save("ozon.xlsx")

infile = open("div_book.xml", 'r')
# infile = open("test.xml", 'r')
context = etree.iterparse(infile, events=("start", "end"))

for event, element in context:
    if event == "end":
        if element.tag == "offer":
            r += 1
            a = element.findtext('name')
            b = element.findtext('url')
            b = '%s?partner=lmr' % b.split('?')[0]
            c = element.findtext('price')
            write('A', r, ws, a)
            write('B', r, ws, b)
            write('C', r, ws, c)
            wb.save("ozon.xlsx")


#
# name = xml.getElementsByTagName('name')
# url = xml.getElementsByTagName('url')
# price = xml.getElementsByTagName('price')
#
#
#
# # names = []
# for title in name:
#     t = title.childNodes[0].nodeValue
#     t = t.encode('cp1251')
#     print t
    # names.append(t)

# urls = []
# for u in url:
#     source = u.childNodes[0].nodeValue
#     source = '%s?partner=lmr' % source.split('?')[0]
#     urls.append(source)
#
# prices = []
# for p in price:
#     pr = p.childNodes[0].nodeValue
#     prices.append(pr)
#
# r = zip(names, urls, prices)
#
# for a in r:
#     writer.writerow([a[0], a[1], a[2]])
