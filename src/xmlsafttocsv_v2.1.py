import xml.etree.ElementTree as ET
import csv
import sys

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
         find_all_lines(child, "", level+1,  0)
      for child in elem.getchildren():
          find_all_lines(child, "", level+1,  1)
   for child in elem.getchildren():
      find_journal_lines(child, level+1)

def find_all_headers(elem, headerhead, level=0):
   global gllevel, headerslen
   elemtag = elem.tag.split("}")[1][0:]
   elemtext = elem.text
   if headerhead+elemtag not in headers and "\n\t" not in elemtext:
      headers.append(headerhead + elemtag)
      headerslen = headerslen + 1
      sys.stdout.write("+")
   for child in elem.getchildren():
      find_all_headers(child, headerhead + elemtag + "." , level+1)

def find_all_lines(elem, linesline, level=0, linewrite=0):
   global gllevel, headerslen, addline
   elemtag = elem.tag.split("}")[1][0:]
   elemtext = elem.text
   if elemtag == "Line":
      for k in list(addline.keys()):
         if k.startswith("Transaction.Line"):
             del addline[k]
   if "\n\t" not in elemtext and linewrite==0:
      addline[linesline + elemtag] = elemtext
   if linewrite==1:
      for child in elem.getchildren():
         find_all_lines(child, linesline + elemtag + ".", level+1, 0)
         find_all_lines(child, linesline + elemtag + ".", level+1, 1)
   if elemtag == "Line" and linewrite==1:
      csvwriter.writerow([addline.get(col, None) for col in headers])
      sys.stdout.write("+")

tree = ET.parse("saft.xml")
root = tree.getroot()
ns = {'n1': 'urn:StandardAuditFile-Taxation-Financial:NO'}
f = open('out.csv', 'w')
csvwriter = csv.writer(f)

sys.stdout.write("Finding all headers: ")
find_journal_header(root)
sys.stdout.write("\n")
print("All headers found and written")
csvwriter.writerow(headers)
sys.stdout.write("Creating lines: ")
find_journal_lines(root)
sys.stdout.write("\n")
print("Finished...")
