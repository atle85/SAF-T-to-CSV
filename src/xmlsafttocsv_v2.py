import xml.etree.ElementTree as ET
from lxml import objectify
import csv

global headers, headerslen, gllevel, addline
headers = []
headerslen = 0
addline = []

def find_journal_header(elem, level=0):
   global gllevel
   elemtag = elem.tag.split("}")[1][0:]
   elemtext = elem.text
   if elemtag == "Journal":
      gllevel = level
      for child in elem.getchildren():
         find_all_headers(child, "", level+1)
   for child in elem.getchildren():
      find_journal_header(child, level+1)

def find_journal_lines(elem, level=0):
   global gllevel, addline
   elemtag = elem.tag.split("}")[1][0:]
   elemtext = elem.text
   if elemtag == "Journal":
      gllevel = level
      addline = dict((el,0) for el in headers)
      for child in elem.getchildren():
         find_all_lines(child, "", level+1)
   for child in elem.getchildren():
      find_journal_lines(child, level+1)

def find_all_headers(elem, headerhead, level=0):
   global gllevel, headerslen
   elemtag = elem.tag.split("}")[1][0:]
   elemtext = elem.text
   if headerhead+elemtag not in headers and "\n\t" not in elemtext:
      headers.append(headerhead + elemtag)
      headerslen = headerslen + 1
   for child in elem.getchildren():
      find_all_headers(child, headerhead + elemtag + "." , level+1)

def find_all_lines(elem, linesline, level=0, linewrite=0):
   global gllevel, headerslen, addline
   elemtag = elem.tag.split("}")[1][0:]
   elemtext = elem.text
   if elemtag == "Line":
      for k,v in addline.items():
         if k.startswith("Transaction.Line"):
             del addline[k]
   if "\n\t" not in elemtext:
      addline[linesline + elemtag] = elemtext
   for child in elem.getchildren():
      find_all_lines(child, linesline + elemtag + ".", level+1)
   if elemtag == "Line":
      csvwriter.writerow([addline.get(col, None) for col in headers])

tree = ET.parse("saft.xml")
root = tree.getroot()
ns = {'n1': 'urn:StandardAuditFile-Taxation-Financial:NO'}
f = open('out.csv', 'w')
csvwriter = csv.writer(f)

print "Creating headers..."
find_journal_header(root)
csvwriter.writerow(headers)
print "Creating lines..."
find_journal_lines(root)
print "Finished..."
