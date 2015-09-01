__author__ = 'mblair'
import csv
headerRow =['name','email','password','permissions','voicespermission','listeningpermission','group','reviewerOf','distributionLists','delete'];
with open('PerfUsersAllFiltersOn2000.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(headerRow)
    for iterator in range(2, 2001):

        iteratorAsString = str(iterator);
        paddedNumber = iteratorAsString.zfill(5);
        name= 'swPerfUserAllFiltersOn_'+paddedNumber;
        email= name +'+QA1@socialware.com';


        userRow= [name,email,email,'User','User','None','swPerfGroupAllFiltersOn','','','']
        writer.writerow(userRow)
        print userRow