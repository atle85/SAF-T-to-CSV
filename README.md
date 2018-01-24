# SAF-T-to-CSV
Converter in an early stage made for convertering Norwegian SAF-T files to CSV format. 

## Versions
v1) January 17th: Quick mockup/proof of concept.  
v2) January 24th: Converter with a more dynamic design.

## Known bugs
Known bugs in v2:
XML elements occuring in a higher level, but after <n1:Line> will not be
catched and written.

## Install
Download the latest src file. Edit the src file and edit the variables
tree and f to the location of your xml SAF-T file and csv file to be written
to.
