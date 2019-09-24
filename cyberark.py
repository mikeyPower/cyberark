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
import pandas as pd






#Get timestamp of programme execution
now=str(int(time.time()))
str_now=str(datetime.now())

csvFile = sys.argv[1]

csv.field_size_limit(sys.maxsize)


def excel_to_list(files):
    user_stores=[]
    file_name = files # name of your excel file
    df = pd.read_excel(file_name, sheet_name = 0)
    df1 = pd.read_excel(file_name,sheet_name = 0).columns #print header row
    user_stores.append(df1.values.tolist())
    excel_sheet=df.values.tolist() #return excel sheet as a list
    return(excel_sheet,user_stores)

def add_reference_to_list(files):
    count = 1
    new_list=[]
    for row in files:
        row.insert(0,count)
        new_list.append(row)
        count=count+1


    return(new_list)




def see(csvFile):
    with open(csvFile) as csvfile:
        #readCSV = csv.reader(csvfile, delimiter=',')
        readCSV = csv.reader(x.replace('\0', '') for x in csvfile)
        #skip header row
        readCSV.next()
        for row in readCSV:
            datetime.strptime(str(row[1]), '%d/%m/%Y %H:%M')


def sort_list_by_date(csvFile12):
   # print(csvFile12)
    data = sorted(csvFile12, key = lambda row: row[1]) # if i need to convert string datetime to actually date time
                                                       # datetime.strptime(str(row[1]), '%d/%m/%Y %H:%M:%S'))
    return(data)

def find_stores(readCSV,readCSV2,user_stores):
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
    user_retrieves = []
    user_retrieves_dict = {}

    retrieve_store_password = []
    retrieve_store_password.append(["Retrieve Target Account", "Retrieve User", "Retrieve Action","Retrieve Safe"
    ,"Retrieve Target System","User Retrieves","Total Number Retrieves","Total Retrieves","Store Target Account","Store User"
    ,"Store Action","Store Time", "Store Safe","Store Target System","Time Difference","Store Present"])

    store_present=False
    for i in readCSV:
        #we want to skip any lines we have already come accross
        if(i[line_number] not in to_skip):
            #first we want to find all the stores that a user committed
            if(i[action].lower().replace(" ","")=="storepassword"):

                if(i[user].lower().replace(" ","")!="passwordmanager"):
                    user_stores.append(i)


            #if the action is a retireve search the file for its equivant store action on the same target
            if(i[action].lower().replace(" ","")=="retrievepassword"):
                #reset these variable
                store_present=False
                user_retrieves_dict.clear()
                user_retrieves_dict[i[user]]=1
                to_skip.append(i[line_number])
                for j in readCSV2:
                    if(j[line_number] not in to_skip):
                        #if we find the same target as the retireve and if there is a store break the inner loop
                        #and append the result to the list which will be written to an excel file
                        if(i[target].lower().replace(" ","")==j[target].lower().replace(" ","")):
                            to_skip.append(j[line_number])
                            if(j[action].lower().replace(" ","")=="storepassword"):
                                #do something
                                user_stores.append(j)
                                store_present=True
                                break;

                                #if a password retreive found and different user to the ones we've found already append the new user to the list
                            elif(j[action].lower().replace(" ","")=="retrievepassword"):
                                #to_skip.append(j[line_number])
                                if(j[user] not in user_retrieves):
                                    user_retrieves_dict[j[user]]=1
                                else:
                                    user_retrieves_dict[j[user]]=1+user_retrieves_dict[j[user]]

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

                with open('results'+now+'.csv', 'a') as o:
                    writer = csv.writer(o, delimiter=',')
                    if(store_present==True):
                        #calculate the time difference between the retrieve and store of the password
                        #end_date = j[time_of_event].split(" ")[0]
                        #end_time = j[time_of_event].split(" ")[1]
                        #start_date = i[time_of_event].split(" ")[0]
                        #start_time = i[time_of_event].split(" ")[1]

                        #time_dif = str(datetime(int(end_date.split("/")[2]),int(end_date.split("/")[1]),int(end_date.split("/")[0]))-datetime(int(start_date.split("/")[2]),
                        #int(start_date.split("/")[1]),int(start_date.split("/")[0])))

                        time_dif = j[time_of_event]-i[time_of_event]

                        writer.writerow([i[time_of_event],i[user],i[action],i[safe],i[target],i[target_platform],i[target_system],i[target_account],i[new_target],i[reason],
                        i[alert],i[request_id],i[client_id],j[time_of_event],j[user],j[action],j[safe],j[target],j[target_platform],j[target_system],j[target_account],j[new_target],j[reason],
                        j[alert],j[request_id],j[client_id],user_retrieves_dict,sum(user_retrieves_dict.values()),len(user_retrieves_dict),time_dif,"Store Present"])

                        retrieve_store_password.append([i[time_of_event],i[user],i[action],i[safe],i[target],i[target_platform],i[target_system],i[target_account],i[new_target],i[reason],
                        i[alert],i[request_id],i[client_id],j[time_of_event],j[user],j[action],j[safe],j[target],j[target_platform],j[target_system],j[target_account],j[new_target],j[reason],
                        j[alert],j[request_id],j[client_id],user_retrieves_dict,sum(user_retrieves_dict.values()),len(user_retrieves_dict),time_dif,"Store Present"])


                    else:

                        writer.writerow([i[time_of_event],i[user],i[action],i[safe],i[target],i[target_platform],i[target_system],i[target_account],i[new_target],i[reason],
                        i[alert],i[request_id],i[client_id],user_retrieves_dict,sum(user_retrieves_dict.values()),len(user_retrieves_dict),"No Store"])

                        retrieve_store_password.append([i[time_of_event],i[user],i[action],i[safe],i[target],i[target_platform],i[target_system],i[target_account],i[new_target],i[reason],
                        i[alert],i[request_id],i[client_id],user_retrieves_dict,sum(user_retrieves_dict.values()),len(user_retrieves_dict),"No Store"])


                o.close()



        # if in skip go to next interation of most outer loop
        else:
            pass

    return(user_stores,retrieve_store_password)


def write_nested_list_to_excel(user_stores,retrieve_store_password,reference_to_excel):
    df1 = pd.DataFrame(user_stores)
    df2 = pd.DataFrame(retrieve_store_password)
    df3 = pd.DataFrame(reference_to_excel)
    print(reference_to_excel)
    # Give a header row for each sheet
    with pd.ExcelWriter('output.xlsx') as writer:  # doctest: +SKIP
        df1.to_excel(writer, sheet_name='Sheet_name_1',header=False,index=False)
        df2.to_excel(writer, sheet_name='Sheet_name_2',header=False,index=False)
        df3.to_excel(writer, sheet_name='Sheet_name_3',header=False,index=False)



#main(csvFile)
a,user_stores = excel_to_list(csvFile)
b=sort_list_by_date(a)
c=add_reference_to_list(b)
user_stores_1,retrieve_store_password=find_stores(c,c,user_stores)
user_stores[0].insert(0,"Ref")
write_nested_list_to_excel(user_stores_1,retrieve_store_password,user_stores+c)
