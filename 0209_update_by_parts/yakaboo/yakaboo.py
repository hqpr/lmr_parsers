from xml.dom.minidom import *
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

wb.save("yakaboo.xlsx")

xml = parse('partner_export_books.xml')
name = xml.getElementsByTagName('title')
url = xml.getElementsByTagName('url')
price = xml.getElementsByTagName('price')

for title in name:
    t = title.childNodes[0].nodeValue
    r += 1
    write('A', r, ws, t)

for u in url:
    source = u.childNodes[0].nodeValue
    yakaboo = source.replace('{puser}', '')
    yakaboo = '%sowl/' % yakaboo
    r += 1
    write('B', r, ws, yakaboo)

for p in price:
    pr = p.childNodes[0].nodeValue
    r += 1
    write('C', r, ws, pr)
wb.save("yakaboo.xlsx")
