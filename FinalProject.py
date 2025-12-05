"""
Court Data Processing Application v3.0 (Final)

Features:
- GUI with ttkbootstrap (Modern Look)
- Handles 3 text files
- Auto-detects Bond, Charges, Fingerprint status
- Professional Excel Export (Auto-width, Filter arrows, Banded rows)

By Connor Soucey and Jared Towery
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as tb 
from ttkbootstrap.constants import *
import os
import re
import pandas as pd
import xlsxwriter

# --- RegEx Pattern Definitions ---
header_pattern = r"RUN DATE:\s+(\d+\/\d+\/\d+).*PAGE\s+(\d+)"
sh_pattern = r"COURT DATE:\s+(\d+\/\d+\/\d+).*TIME:\s+(\d+:\d+\s+\w+).*COURTROOM NUMBER:\s+(\w+)"
data_pattern = r"(\d+)\s+(\w+\s+\d+)\s+(\S+)\s+(\S+)\s+ATTY:(\S+)\s+(\d+)+"
data2_pattern = r"BOND:\s+(\$\d+)?\s*([A-Z]{3})"
data3_pattern = r"(\([TIM]\).*?)\s+PLEA:(.*?)\s+VER:(.*)"
data4_pattern = r"CLS:(.*?)\s+P:(.*?)\s+L:(.*?)\s+JUDGMENT:(.*)"
fingerprint_pattern = r"DEFENDANT NEEDS TO BE FINGERPRINTED"

class CourtApp:

    def center_window(self, width=600, height=350):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def __init__(self, root):
        self.root = root
        self.root.title("Court Data Processor v3.0")
        self.center_window(650, 400)
        self.root.columnconfigure(1, weight=1)
 
        # Title Label
        tb.Label(root,  text="Select Court Text Files (Up to 3)", font=("Arial", 14, "bold"), bootstyle="primary").grid(row=0, column=0, columnspan=3, pady=20)

        # File 1
        tb.Label(root,  text="File 1:").grid(row=1, column=0, padx=10, sticky="e")
        self.entry1 = tb.Entry(root, width=55)
        self.entry1.grid(row=1, column=1, padx=5)
        tb.Button(root, text="Browse", bootstyle="outline", command=lambda: self.browse_file(self.entry1)).grid(row=1, column=2, padx=5)

        # File 2 
        tb.Label(root,  text="File 2:").grid(row=2, column=0, padx=10, sticky="e")
        self.entry2 = tb.Entry(root, width=55)
        self.entry2.grid(row=2, column=1, padx=5)
        tb.Button(root, text="Browse", bootstyle="outline", command=lambda: self.browse_file(self.entry2)).grid(row=2, column=2, padx=5)

        # File 3
        tb.Label(root,  text="File 3:").grid(row=3, column=0, padx=10, sticky="e")
        self.entry3 = tb.Entry(root, width=55)
        self.entry3.grid(row=3, column=1, padx=5)
        tb.Button(root, text="Browse", bootstyle="outline", command=lambda: self.browse_file(self.entry3)).grid(row=3, column=2, padx=5)

        # Process Button
        process_btn = tb.Button(root, 
                                text="PROCESS DATA & EXPORT", 
                                bootstyle="success", 
                                width=25,
                                command=self.process_data)
        process_btn.grid(row=4, column=0, columnspan=3, pady=30)

    def browse_file(self, entry_field):
        """Opens file dialog and inserts path into the entry box"""
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filename:
            entry_field.delete(0, tk.END)
            entry_field.insert(0, filename)

    def process_data(self):
        # File Collection
        files = []
        if self.entry1.get(): files.append(self.entry1.get())
        if self.entry2.get(): files.append(self.entry2.get())
        if self.entry3.get(): files.append(self.entry3.get())

        if not files:
            messagebox.showerror("Error", "Please select at least one file.")
            return

        # Remove old output
        try:    
            if os.path.exists('Court_Output.xlsx'):
                os.remove('Court_Output.xlsx')
        except PermissionError:
            messagebox.showerror("Error", "Please close 'Court_Output.xlsx' before running.")
            return

        # Data Processing 
        master = []
        current_header = {'court_date': None, 'time': None,'court_num': None}
        report_header = {'run_date': None, 'page': None}
        current_data = {'no':None,'file_number':None,'def_name':None,'complainant':None,'attorney':None,'cont':None}
        current_data2 = {'bond':None,'bond_type':None}

        for textfile in files:
            try:
                with open(textfile, "r") as f:      
                    content = f.read().splitlines()
            except FileNotFoundError:
                print(f"Skipping {textfile}")
                continue

            current_data2 = {'bond':None,'bond_type':None}

            for line in content:
                # Header
                header_match = re.search(header_pattern, line)
                if header_match:
                    report_header['run_date'] = header_match.group(1)
                    report_header['page'] = header_match.group(2)

                # Page Header
                sh_match = re.search(sh_pattern,line)
                if sh_match:
                    current_header['court_date'] = sh_match.group(1)
                    current_header['time'] = sh_match.group(2)
                    current_header['court_num'] = sh_match.group(3)

                # Case Data
                data_match = re.search(data_pattern,line)
                if data_match:
                    current_data['no'] = data_match.group(1)
                    current_data['file_number'] = data_match.group(2)
                    current_data['def_name'] = data_match.group(3)
                    current_data['complainant']= data_match.group(4)
                    current_data['attorney']= data_match.group(5)
                    current_data['cont']= data_match.group(6)

                    row = {'Run Date':report_header['run_date'],
                           'Page':report_header['page'],
                           'Court Date':current_header['court_date'],
                           'Time': current_header['time'],
                           'Courtroom': current_header['court_num'],
                           'Case Number':current_data['no'],
                           'File Number': current_data['file_number'],
                           'Defendant Name':current_data['def_name'],
                           'Complaintant':current_data['complainant'],
                           'Attorney':current_data['attorney'],
                           'Continuances':current_data['cont'],
                           'Needs Fingerprinted': 'No',
                           'Charge': None, 'Plea': None, 'Ver': None,
                           'Bond': None, 'Bond Type': None,
                           'CLS': None, 'P': None, 'L': None, 'Judgment': None
                           }
                    master.append(row)
                    current_data2 = {'bond':None,'bond_type':None}

                # Fingerprint
                if re.search(fingerprint_pattern, line):
                    if master: master[-1]['Needs Fingerprinted'] = 'Yes'

                # Bond
                data2_match = re.search(data2_pattern,line)
                if data2_match:
                    current_data2['bond'] = data2_match.group(1) if data2_match.group(1) else ""
                    current_data2['bond_type'] = data2_match.group(2)
                    if master:
                        master[-1]['Bond'] = current_data2['bond']
                        master[-1]['Bond Type'] = current_data2['bond_type']

                # Charge
                data3_match = re.search(data3_pattern,line)
                if data3_match:
                    new_charge = data3_match.group(1).strip()
                    new_plea = data3_match.group(2).strip()
                    new_verdict = data3_match.group(3).strip()

                    if master:
                        last_row = master[-1]
                        if last_row['Charge'] is None:
                            last_row['Charge'] = new_charge
                            last_row['Plea'] = new_plea
                            last_row['Ver'] = new_verdict
                        else:
                            row_copy = last_row.copy()
                            row_copy['Charge'] = new_charge
                            row_copy['Plea'] = new_plea
                            row_copy['Ver'] = new_verdict
                            row_copy['CLS'] = None; row_copy['P'] = None; row_copy['L'] = None; row_copy['Judgment'] = None
                            master.append(row_copy)

                # Judgment
                data4_match = re.search(data4_pattern, line)
                if data4_match and master:
                    master[-1]['CLS'] = data4_match.group(1).strip()
                    master[-1]['P'] = data4_match.group(2).strip()
                    master[-1]['L'] = data4_match.group(3).strip()
                    master[-1]['Judgment'] = data4_match.group(4).strip()

        # 4. EXPORT LOGIC (Fixed for Professional Output)
        if master:
            df = pd.DataFrame(master)
            cols = ['Court Date', 'Time', 'Courtroom', 'Case Number', 'File Number', 
                    'Defendant Name', 'Complaintant', 'Attorney', 'Continuances',
                    'Needs Fingerprinted', 'Bond','Bond Type',
                    'Charge','Plea','Ver', 'CLS', 'P', 'L', 'Judgment']
            
            df = df.reindex(columns=cols)
            
            # --- START XLSWRITER FORMATTING ---
            
            # 1. Create the writer
            writer = pd.ExcelWriter('Court_Output.xlsx', engine='xlsxwriter')
            
            # 2. Write data to 'Court Data' sheet (index=False hides the row numbers 0,1,2...)
            sheet_name = 'Court Data'
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # 3. Get the objects to apply formatting
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            (max_row, max_col) = df.shape
            
            # 4. Add the Table (This adds the blue headers and arrows)
            column_settings = [{'header': col} for col in df.columns]
            worksheet.add_table(0, 0, max_row, max_col - 1, {
                'columns': column_settings,
                'style': 'Table Style Medium 2',
                'name': 'CourtTable'
            })
            
            # 5. Auto-adjust column width (Makes text readable)
            for i, col in enumerate(df.columns):
                # Calculate width based on max length of data in that column
                max_len = max(df[col].astype(str).map(len).max(), len(col))
                worksheet.set_column(i, i, max_len + 2) # +2 for padding

            # 6. Save
            writer.close()
            
            # --- SUCCESS MESSAGE & AUTO OPEN ---
            msg = f"Success! Processed {len(master)} records.\nSaved to 'Court_Output.xlsx'"
            launch_excel = messagebox.askyesno("Processing Complete", msg + "\n\nWould you like to open the file now?")
            
            if launch_excel:
                try:
                    os.startfile('Court_Output.xlsx')
                except Exception as e:
                    print(f"Could not open Excel automatically: {e}")
                
        else:
            messagebox.showwarning("Warning", "No data found in the selected files.")

if __name__ == "__main__":
    # Themes: minty, superhero, journal, united, darkly
    root = tb.Window(themename="minty") 
    app = CourtApp(root)
    root.mainloop()