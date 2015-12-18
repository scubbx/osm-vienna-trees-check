"""
This script loads the ODG trees CSV file into a CouchDB database
"""

import mpcouch
import csv

ifile = open('baumkataster151217_converted.csv', "r")
reader = csv.reader(ifile, delimiter=',', quotechar='"')

countfile = open('baumkataster151217_converted.csv', "r")
print("Calculate total amount of entries")
rowcount = len(list(csv.reader(countfile))) 

couchPusher = mpcouch.mpcouchPusher("http://gi88.geoinfo.tuwien.ac.at:5984/osmnodesvienna",30000,threads = False, jobsbuffersizemax = 20)

def gotCompleteEntry(entry):
    # couchPusher.pushData({'data':entry, '_id': entry[0]['version'] + '-' + entry[0]['id']})
    couchPusher.pushData({'data':entry, 'source': 'ogd'})
    #print(entry)

rownum = 0
for row in reader:
    if rownum % 10000 == 0: print("     Imported {} of {} thousand".format(int(rownum/1000), int(rowcount/1000)))
    if rownum == 0:
        header = row
        print(header)
    else:
        treeData = {'x': row[0], 'y': row[1], 'natural': row[2], 'tree:ref': row[3], 'species': row[4], 'species:de': row[5], 'circumference': row[6], 'height': row[7], 'diameter_crown': row[8], 'type': row[9], 'taxon:cultivar': row[10], 'Taxon': row[11], 'start_date': row[12], 'fixme': row[13], 'source': row[14]}
        gotCompleteEntry(treeData)
    rownum += 1

couchPusher.finish()
