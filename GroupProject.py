"""Court Data Processing Application
A simple python program for converting .txt format court documents to .xlsx format
By Connor Soucey and Jared Towery
11/17/2025
Last Modified: 12/4/2025"""

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
data_pattern = r"(\d+)\s+(\w+\s+\d+)\s+(\S+)\s+(\S+)\s+ATTY:(\S+)\s+(\d+)+"
data2_pattern = r"BOND:\s+(\$\d+)\s+([A-Z]{3})"
data3_pattern = r"\(T\)\s*(.*?)\s+PLEA:\s*(.*?)\s*VER:\s*(.*)"

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
        #Process report header
        header_match = re.search(header_pattern, line)
        if header_match:
            report_header['run_date'] = header_match.group(1)
            report_header['page'] = header_match.group(2)
            print(report_header)

        #Process page headers
        sh_match = re.search(sh_pattern,line)
        if sh_match:
            current_header['court_date'] = sh_match.group(1)
            current_header['time'] = sh_match.group(2)
            current_header['court_num'] = sh_match.group(3)
            print(current_header)

        #Process case data
        data_match = re.search(data_pattern,line)
        if data_match:
            current_data['no'] = data_match.group(1)
            current_data['file_number'] = data_match.group(2)
            current_data['def_name'] = data_match.group(3)
            current_data['complaintant']= data_match.group(4)
            current_data['attorney']= data_match.group(5)
            current_data['cont']= data_match.group(6)
            print(current_data)

            row = {'Run Date':report_header['run_date'],
                   'Page':report_header['page'],
                   'Court Date':current_header['court_date'],
                   'Time': current_header['time'],
                   'Courtroom': current_header['court_num'],
                   'Case Number':current_data['no'],
                   'File Number': current_data['file_number'],
                   'Defendant Name':current_data['def_name'],
                   'Complaintant':current_data['complaintant'],
                   'Attorney':current_data['attorney'],
                   'Continuances':current_data['cont'],
                   'Charge': None,
                   'Plea': None,
                   'Verdict': None,
                   'Bond': None,
                   'Bond Type': None
                   }
            
            master.append(row)

            #Resets bond data for next case
            current_data2 = {'bond':None,'bond_type':None}

        #process bond data
        data2_match = re.search(data2_pattern,line)
        if data2_match:
            current_data2['bond'] = data2_match.group(1)
            current_data2['bond_type'] = data2_match.group(2)
            print(data2_match)
            if master:
                master[-1]['Bond'] = current_data2['bond']
                master[-1]['Bond Type'] = current_data2['bond_type']

        #Process charge data
        data3_match = re.search(data3_pattern,line)
        if data3_match:

            #Handling multiple charges
            new_charge = data3_match.group(1).strip()
            new_plea = data3_match.group(2)
            new_verdict = data3_match.group(3)


            if master:
                last_row = master[-1]

                if last_row['Charge'] is None:

                    last_row['Charge'] = new_charge
                    last_row['Plea'] = new_plea
                    last_row['Verdict'] = new_verdict

                else:

                    row_copy = last_row.copy()
                    
                    row_copy['Charge'] = new_charge
                    row_copy['Plea'] = new_plea
                    row_copy['Verdict'] = new_verdict
                    
                    master.append(row_copy)
            

        
    if master:
        df = pd.DataFrame(master)
        cols = ['Court Date', 'Time', 'Courtroom', 'Case Number', 'File Number', 'Defendant Name', 'Complaintant', 'Attorney', 'Continuances','Bond','Bond Type','Charge','Plea','Verdict']
        df = df[cols]
        df.to_excel('test.xlsx',sheet_name='Data',index=False)
def main():
    parseData()

if __name__ == '__main__':
    main()
