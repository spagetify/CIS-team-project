""""""

#Imports
import breezypythongui
import os
import re

def importText(textfile):
    try:
        with open(textfile,"r") as f:
            for line in f:
                break
            if line.__contains__("RUN DATE:"):
                count = 0 
                for line in f:
                    print(line.strip())
                    count +=1
                    if count>16:
                        break

                    
                    
                    
            content = f.read()

            match = re.findall(r'<RUN >(\n|.)*?</IN>', textfile)
            print(match)

            

    except(ValueError):
        print("valueerror")


#atty_pattern = r"ATTY:[a-zA-Z]+,*[a-zA-Z]*"
#name_pattern = r"^(?!ATTY:).*[a-zA-Z]+,[a-zA-Z]*+,[a-zA-Z]*"
#name_match = re.findall(name_pattern, content)



importText('11test.txt')

def main():
    return
if __name__ == '__main__':
    main()
