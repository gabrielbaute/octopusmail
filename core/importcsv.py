import csv

def importcsv(filepath):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        receivers = list(reader)
    
    return receivers