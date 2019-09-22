#!/usr/bin/python

#1.first need to sort file by date
#2.then see how long a password has been out for
#    to see how long a password has been out for we look at the target system
#    we are focused on the date, user, acton and target column for this
#    before entering the second loop the inner loop will be a line ahead of the outer loop
#    when looping through the inner loop we will take note of the target column
#    when we hit the same target as to the retrieve password we are on take note of the line number, the user, the action
#        if the acton is a store calculate the time period
#        write to a file the user who took it out, who stored it, the time period and also the reason it was taken out, stored and how many different user
#        retrieved it before the store
#        if we come to the end of the file and there has been no store write that line to the new file with a note column detailing that
#        for all those line numbers that we noted between the intial retrieve and if there was a store or delete them from the file
#3. the file should now point to the next line we are looking at and repeat step 2 until we've reached the end of the file


import csv
import sys
from datetime import datetime
import time
import os


line_number = 0
time_of_event = 1
user = 2
action = 3
safe = 4
target = 5
target_platform = 6
target_system = 7
target_account = 8
new_target = 9
reason = 10
alert = 11
request_id = 12
client_id = 13

user_stores = []
to_skip = []
user_retrieves = []
retrieve_store_password = []
store_present=False

#Get timestamp of programme execution
now=str(int(time.time()))
str_now=str(datetime.now())

csvFile = sys.argv[1]

csv.field_size_limit(sys.maxsize)

with open(csvFile) as csvfile:
    #readCSV = csv.reader(csvfile, delimiter=',')
    readCSV = csv.reader(x.replace('\0', '') for x in csvfile)

    #skip header row
    readCSV.next()
    for i in readCSV:
        #we want to skip any lines we have already come accross
        if(i[line_number] not in to_skip):

            #first we want to find all the stores that a user committed
            if(i[action].lower().replace(" ","")=="storepassword"):
                print("action", i[action])
                if(i[user].lower().replace(" ","")!="passwordmanager"):
                    user_stores.append(i[user])
                    print("user found", i[user])

                    #if the action is a retireve search the file for its equivant store action on the same target
            if(i[action].lower().replace(" ","")=="retrievepassword"):
                #print("action1", i[action])
                with open(csvFile) as csvfile1:
                    readCSV2 = csv.reader(x.replace('\0', '') for x in csvfile1)
                    #skip header row
                    readCSV2.next()

                    #reset these variables
                    store_present=False
                    del user_retrieves[:]
                    #ruser_retrieves.clear()
                    to_skip.append(i[line_number])
                    for j in readCSV2:
                        if(j[line_number] not in to_skip):

                            #if we find the same target as the retireve and if there is a store break the inner loop
                            #and append the result to the list which will be written to an excel file

                            if(i[target].lower().replace(" ","")==j[target].lower().replace(" ","")):

                                to_skip.append(j[line_number])
                                if(j[action].lower().replace(" ","")=="storepassword"):
                                    #do something
                                    store_present=True

                                    break;

                                    #if a password retreive found and different user to the ones we've found already append the new user to the list
                                elif(j[action].lower().replace(" ","")=="retrievepassword" and j[user] not in user_retrieves):
                                    print(user_retrieves)
                                    user_retrieves.append(j[user])

                                    #skip everything that is not a store or retreive password action
                                else:
                                    pass
                                    #if different target the target found in outer loop skip until we find the identical target
                            else:
                                pass
                        else:
                            pass

                    #if a store is found for the coressponding retreive we want to store the result indicating just that
                    #else indicate we have gone through the entire file and no store found
                    print(user_retrieves)
                    with open('results'+now+'.csv', 'a') as o:
                        writer = csv.writer(o, delimiter=',')
                        if(store_present==True):
                            #calculate the time difference between the retrieve and store of the password
                            end_date = j[time_of_event].split(" ")[0]
                            end_time = j[time_of_event].split(" ")[1]
                            start_date = i[time_of_event].split(" ")[0]
                            start_time = i[time_of_event].split(" ")[1]

                            time_dif = str(datetime(int(end_date.split("/")[2]),int(end_date.split("/")[1]),int(end_date.split("/")[0]))-datetime(int(start_date.split("/")[2]),
                            int(start_date.split("/")[1]),int(start_date.split("/")[0])))

                            writer.writerow([i[time_of_event],i[user],i[action],i[safe],i[target],i[target_platform],i[target_system],i[target_account],i[new_target],i[reason],
                            i[alert],i[request_id],i[client_id],j[time_of_event],j[user],j[action],j[safe],j[target],j[target_platform],j[target_system],j[target_account],j[new_target],j[reason],
                            j[alert],j[request_id],j[client_id],user_retrieves,time_dif,"Store Present"])
                            #print(retrieve_store_password)
                        else:

                            writer.writerow([i[time_of_event],i[user],i[action],i[safe],i[target],i[target_platform],i[target_system],i[target_account],i[new_target],i[reason],
                            i[alert],i[request_id],i[client_id],user_retrieves,"No Store"])
                            #print(retrieve_store_password)
                    o.close()
                csvfile1.close()


        #go to next interation of most outer loop
        else:
            pass
csvfile.close()
