import csv

def importcsv(filepath):
    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        
        reader=csv.DictReader(csvfile)
        receivers=[]
        
        for row in reader:
            if "email" in row and "name" in row:
                receivers.append(row)
            else:
                print(f"Missing keys in row: {row}")
    
    return receivers