# cyberark
Cyberark is a publicly traded information security company offering Privileged Account Security, one such aplication that Cyberark offer is in the form of a password vault. The code in this repo demonstrates how to analyse the logs of this password vault.

## Prerequisite
python 3.7.0

To install the following libraries run the follwing command

    pip3 install pandas
Or run the following shell script

    ./install.sh
## Header for Input File

| Time  | User | Action | Safe | Target | Target Platform | Target System | Target Account | New Target | Reason | Alert | Request ID | Client ID |
| ----- | ---- | ------ | ---- | ------ | --------------- | ------------- | -------------- | ---------- | ------ | ----- | ---------- | ------------ | 
    
## Run
    $ python3 cyberark.py log1.xlsx
    lenght of log1.xlsx:  11
    Outputed File:  output1588944091.xlsx
    Execution Time:  0.958949089050293
    
## Output file

The output file is an excel file with 3 tabs:<br/>

    1. User Stores: Is a tab that contains all the users that stored a password excluding those of Password Manager<br/>
    
    2. Retrieves: This tab contains information regarding all the passwords that were taken out and if there was an equivalent      store<br/>
    
       action for that password taking into account of any other user who took the password out while a store had not occured<br/>
       
    3. Ref Safe: This tab is the original input file after it has been sorted used in order to reference our findings for the above two tabs discussed previously
    
    
