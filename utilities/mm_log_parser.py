__author__ = 'mblair'

import re

# with open('../results/results_2015.08.18_15.19.14/results.csv', 'r+') as f:
# data = mmap.mmap(f.fileno(), 0)
# mo = re.search('\\d+,\\d+.\\d*,\\d*,.*,\\d*.\\d*,,{}', data)
# if mo:
# print data. #"found error", mo.group(1)


listOfErrors = dict()
f = open('../results/latest/results.csv', 'r')
for eachLine in f:
    martchedString = re.search('\\d+,\\d+.\\d*,\\d*,.*,\\d*.\\d*,,{}', eachLine)
    if not martchedString:
        #print martchedString.group(1)
        errorString = re.search('\d+,\d+.\d*,\d*,.*,\d*.\d*,(.*),{}',eachLine).group(1)
        #print errorString
        if errorString in listOfErrors:
             listOfErrors[errorString] += 1
        else:
             listOfErrors[errorString] = 1
        #print errorString.string.group(1)
        #print errorString
        #listOfErrors.append(eachline)
        #print eachline

print "Errors:"
for errorKey in listOfErrors:
    print str(format(listOfErrors[errorKey],",d")).rjust(12)+":   "+errorKey