import xml.etree.ElementTree as ET
import csv

tree = ET.parse("saft.xml")
root = tree.getroot()
ns = {'n1': 'urn:StandardAuditFile-Taxation-Financial:NO'}

f = open('out.csv', 'w')

csvwriter = csv.writer(f)

count = 0

head = ['JournalID','JournalDescription','LineAccount','LineDebit','LineCredit']

csvwriter.writerow(head)

journalcount = 0
linecount = 0
for journal in root.findall('n1:GeneralLedgerEntries/n1:Journal', ns):
    journalcount = 1 + journalcount
    print "nummer : ",journalcount
    journal_id = journal.find("n1:JournalID", ns).text
    journal_description = journal.find("n1:Description", ns).text
    for line in journal.findall('n1:Transaction/n1:Line', ns):
       row = []
       linecount = linecount + 1
       print "line : ",linecount
       row.append(journal_id)
       row.append(journal_description)
       journallineaccount = line.find("n1:AccountID", ns).text
       row.append(journallineaccount)
       if line.find("n1:DebitAmount/n1:Amount", ns) is None:
          journallinedebit = 0
       else:
          journallinedebit = line.find("n1:DebitAmount/n1:Amount", ns).text
       row.append(journallinedebit)
       if line.find("n1:CreditAmount/n1:Amount", ns) is None:
          journallinecredit = 0
       else:
          journallinecredit = line.find("n1:CreditAmount/n1:Amount", ns).text
       row.append(journallinedebit)
       row.append(journallinecredit)
       csvwriter.writerow(row)

f.close()
