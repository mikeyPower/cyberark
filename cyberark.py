#!/usr/bin/python

1.first need to sort file by date
2.then see how long a password has been out for
    to see how long a password has been out for we look at the target system
    we are focused on the date, user, acton and target column for this
    before entering the second loop the inner loop will be a line ahead of the outer loop
    when looping through the inner loop we will take note of the target column
    when we hit the same target as to the retrieve password we are on take note of the line number, the user, the action
        if the acton is a store calculate the time period
        write to a file the user who took it out, who stored it, the time period and also the reason it was taken out, stored and how many different user
        retrieved it before the store
        if we come to the end of the file and there has been no store write that line to the new file with a note column detailing that
        for all those line numbers that we noted between the intial retrieve and if there was a store or delete them from the file
3. the file should now point to the next line we are looking at and repeat step 2 until we've reached the end of the file


import csv
import sys
from datetime import datetime
import time
import os

#Get timestamp of programme execution
now=str(int(time.time()))
str_now=str(datetime.now())

csvFile = sys.argv[1]

csv.field_size_limit(sys.maxsize)

with open(csvFile) as csvfile:
    #readCSV = csv.reader(csvfile, delimiter=',')
    readCSV = csv.reader(x.replace('\0', '') for x in csvfile)
    #readCSV2 = readCSV
    for i in readCSV:
        #readCSV.seek(0)
        for j in readCSV:
            print(i)
