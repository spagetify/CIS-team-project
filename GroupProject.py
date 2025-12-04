""""""


# Regex pattern examples for reference purposes 
# -----DELETE ME BEFORE SUBMITTING-----
# 1. "Order ID:\s+"  -> Match the literal words and spaces (\s+)
# 2. (\d+)           -> GROUP 1: Capture the digits (The ID)
# 3. ".*Total:\s+"   -> Match junk characters (.*) until "Total: "
# 4. (\$\d+\.\d+)    -> GROUP 2: Capture the price ($ + digits + dot + digits)
# 5. ".*Status:\s+"  -> Match junk until "Status: "
# 6. (\w+)           -> GROUP 3: Capture the word characters (The Status)

#pattern = r"Order ID:\s+(\d+\/\d+\/\d+).*Total:\s+(\$\d+\.\d+).*Status:\s+(\w+)"

#Imports
import breezypythongui
import os
import re
import pandas as pd

master = []
current_header = {'court_date': None, 'time': None,'court_num': None}
report_header = {'run_date': None, 'page': None}
current_data = {'no':None,'file':None,'number':None,'def_name':None,'complaintant':None,'attorney':None,'cont':None}
current_data2 = {'bond':None,'bond_type':None}

try:    
    os.remove('test.xlsx')
except(FileNotFoundError):
    print("File Already removed")

#RegEx Pattern Definitions
header_pattern = r"RUN DATE:\s+(\d+\/\d+\/\d+).*PAGE\s+(\d+)"
sh_pattern = r"COURT DATE:\s+(\d+\/\d+\/\d+).*TIME:\s+(\d+:\d+\s+\w+).*COURTROOM NUMBER:\s+(\w+)"
data_pattern = r"(\d+)\s+(\w+)\s+(\d+)\s+(\S+)\s+(\S+)\s+ATTY:(\S+)\s+(\d+)+"
data2_pattern = r"BOND:\s+(\$\d+)\s+([A-Z]{3})"

#Open and Read the text file
textfile = input("Input The File Name (.txt): ")
try:
    with open(textfile,"r") as f:      
        content = f.read().splitlines() 

except(FileNotFoundError):
    print("File Not Found")

#Processes the header, returns header info
def process_header():
    print("processing header")

def parseData():
    current_data2 = {'bond':None,'bond_type':None}
    for line in content:
        header_match = re.search(header_pattern, line)
        if header_match:
            report_header['run_date'] = header_match.group(1)
            report_header['page'] = header_match.group(2)
            print(report_header)

        sh_match = re.search(sh_pattern,line)
        if sh_match:
            current_header['court_date'] = sh_match.group(1)
            current_header['time'] = sh_match.group(2)
            current_header['court_num'] = sh_match.group(3)
            print(current_header)

        data2_match = re.search(data2_pattern,line)
        if data2_match:
            current_data2['bond'] = data2_match.group(1)
            current_data2['bond_type'] = data2_match.group(2)
            print(data2_match)
            if master:
                master[-1]['Bond'] = current_data2['bond']
                master[-1]['Bond Type'] = current_data2['bond_type']
        data_match = re.search(data_pattern,line)
        if data_match:
            current_data['no'] = data_match.group(1)
            current_data['file'] = data_match.group(2)
            current_data['number'] = data_match.group(3)
            current_data['def_name'] = data_match.group(4)
            current_data['complaintant']= data_match.group(5)
            current_data['attorney']= data_match.group(6)
            current_data['cont']= data_match.group(7)
            print(current_data)

            row = {'Run Date':report_header['run_date'],
                   'Page':report_header['page'],
                   'Court Date':current_header['court_date'],
                   'Time': current_header['time'],
                   'Courtroom': current_header['court_num'],
                   'Case Number':current_data['no'],
                   'File': current_data['file'],
                   'Number':current_data['number'],
                   'Defendant Name':current_data['def_name'],
                   'Complaintant':current_data['complaintant'],
                   'Attorney':current_data['attorney'],
                   'Continuances':current_data['cont'],
                   }
            
            master.append(row)
            current_data2 = {'bond':None,'bond_type':None}
            

        
    if master:
        df = pd.DataFrame(master)
        cols = ['Court Date', 'Time', 'Courtroom', 'Case Number', 'File', 
            'Number', 'Defendant Name', 'Complaintant', 'Attorney', 'Continuances','Bond','Bond Type']
        df = df[cols]
        df.to_excel('test.xlsx',sheet_name='Data',index=False)
def main():
    parseData()

if __name__ == '__main__':
    main()
