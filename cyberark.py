#!/usr/bin/python

#initial logic:
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
import pandas as pd

#Get timestamp of programme execution
#str_now=int(str(datetime.now()))
now = str(int(time.time()))
input_file = sys.argv[1]


#Parameters: takes a single excel file
#Returns: two 2d list
#Method: Takes one excel file and returns both the header
#        and the data as two seperate lists
def excel_to_list(excel_file):
    header=[]
    file_name = excel_file
    #convert excel file to dataframe
    df = pd.read_excel(file_name,header=0,sheet_name = 0)
    #get header row
    df1 = pd.read_excel(file_name,sheet_name = 0).columns
    #return dataframe as a list
    header.append(df1.values.tolist())
    excel_sheet=df.values.tolist()
    return(excel_sheet,header)

#Parameters:2d list
#Returns: 2d list
#Method: Takes a single 2d list and adds an incremental value to the start
#         of each list, as a reference key
def add_reference_to_list(two_d_list):
    count = 1
    new_list=[]
    for row in two_d_list:
        row.insert(0,count)
        new_list.append(row)
        count=count+1
    return(new_list)

#Parameters: 2d list
#Returns: 2d list
#Method: Sorts the list by timestamp
def sort_list_by_date(two_d_list):
    data = sorted(two_d_list, key = lambda row: row[0])
    print(data)
    return(data)

#Parameters: two 2d list
#Returns: two 2d list
#Method: create two instances of a 2d list to search through
#        if we find a store will apend that to one of the list we are searching through
#        once we find a retrieve action, search for the corresponding store taking into
#        account any other user who tried to retrieve it before the store
#        if no store found indicate that in the list likewise if a store is found
def find_stores(two_d_list,user_stores):
    #make a shallow copy of the list
    two_d_list_1=two_d_list[:]
    #initalize column index variables
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
    to_skip = []
    user_retrieves_dict = {}
    retrieve_store_password = []
    retrieve_store_password.append(["Ref Retrieve","Retrieve Time","Retrieve Target Account", "Retrieve User", "Retrieve Action","Retrieve Safe"
    ,"Retrieve Target System","User Retrieves","Total Number Retrieves","Total Users","Ref Store","Store Time","Store Target Account","Store User"
    ,"Store Action", "Store Safe","Store Target System","Time Difference","Store Present"])
    store_present=False
    #Used as reference point to skip to +i of the inner for loop
    count = 0

    for i in two_d_list:
        #we want to skip any lines we have already come accross
        count = count +1
        if(i[line_number] not in to_skip):
            #first we want to find all the stores that a user committed
            if(i[action].lower().replace(" ","")=="storepassword"):
                if(i[user].lower().replace(" ","")!="passwordmanager"):
                    user_stores.append(i)
            #if the action is a retireve search the file for its equivant store action on the same target
            elif(i[action].lower().replace(" ","")=="retrievepassword"):
                #reset these variable
                store_present=False
                user_retrieves_dict.clear()
                user_retrieves_dict[i[user]]=1
                to_skip.append(i[line_number])
                for j in two_d_list_1[count:]:
                    if((j[line_number] not in to_skip)): #and (i[line_number]<j[line_number])):
                        #if we find the same target as the retireve and if there is a store break the inner loop
                        #and append the result to the list which will be written to an excel file
                        if(str(i[target]).lower().replace(" ","")==str(j[target]).lower().replace(" ","")):
                            if(j[action].lower().replace(" ","")=="storepassword"):
                                store_present=True
                                break;
                            #if a password retreive found and different user to the ones we've found already append the new user to the list
                            elif(j[action].lower().replace(" ","")=="retrievepassword"):
                                #want to skip any retreives on the next iteration of the outer loop
                                to_skip.append(j[line_number])
                                #keep track of what and how many times users have retrieved the passwords
                                if(j[user] not in user_retrieves_dict):
                                    user_retrieves_dict[j[user]]=1
                                else:
                                    user_retrieves_dict[j[user]]=1+user_retrieves_dict[j[user]]

                #if a store is found for the coressponding retreive we want to store the result indicating just that
                #else indicate we have gone through the entire file and no store found
                if(store_present==True):
                    #calculate the time difference between the retrieve and store of the password
                    time_dif = j[time_of_event]-i[time_of_event]
                    #converted dict to string as strings are inmutables
                    retrieve_store_password.append([i[line_number],i[time_of_event],i[target_account],i[user],i[action],i[safe],i[target_system],str(user_retrieves_dict),sum(user_retrieves_dict.values()),
                    len(user_retrieves_dict),j[line_number],j[time_of_event],j[target_account],j[user],j[action],j[safe],j[target_system],
                    time_dif,"Store Present"])
                else:
                    retrieve_store_password.append([i[line_number],i[time_of_event],i[target_account],i[user],i[action],i[safe],i[target_system]
                    ,str(user_retrieves_dict),sum(user_retrieves_dict.values()),len(user_retrieves_dict),"-","-","-","-","-","-","-","-","-","No Store"])

    return(user_stores,retrieve_store_password)

#Parameters: three 2d list
#Returns: None
#Method: Writes each 2d list to a seperate sheet in a single excel book
def write_nested_list_to_excel(user_stores,retrieve_store_password,reference_to_excel):
    #convert list to dataframe
    df1 = pd.DataFrame(user_stores)
    df2 = pd.DataFrame(retrieve_store_password)
    df3 = pd.DataFrame(reference_to_excel)
    # Give a header row for each sheet
    with pd.ExcelWriter('output'+now+'.xlsx') as writer:  # doctest: +SKIP
        df1.to_excel(writer, sheet_name='User Stores',header=False,index=False)
        df2.to_excel(writer, sheet_name='Retrieves',header=False,index=False)
        df3.to_excel(writer, sheet_name='Ref Safe',header=False,index=False)

#Add execution time
start=time.time()
excel_list,user_stores = excel_to_list(input_file)
#make a copy of the header line as it stands before the user_stores list is affected by passing to functions
header = user_stores[:]
#add an extra column to the header line
header[0].insert(0,"Ref")
#sort list
sorted_list = sort_list_by_date(excel_list)
#add ref column to list
ref_list =add_reference_to_list(sorted_list)
user_stores,retrieve_store_password=find_stores(ref_list,user_stores)
write_nested_list_to_excel(user_stores,retrieve_store_password,header+ref_list)
finish=time.time()-start
print("lenght of "+input_file+": ",len(excel_list)+1)
print("Outputed File: ",'output'+now+'.xlsx')
print("Execution Time: ",finish)
