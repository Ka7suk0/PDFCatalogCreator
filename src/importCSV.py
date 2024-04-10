import csv
from referencesAndData import archiveCSV

# ____  __  __  ____  _____  ____  ____ 
#(_  _)(  \/  )(  _ \ ( _  )(  _ \(_  _)
# _)(_  )    (  )___/ )(_)(  )   /  )(  
#(____)(_/\/\_)(__)  (____) (_)\_) (__) 
def readCSVFile():
    data = []
    with open(archiveCSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

productsList = readCSVFile()
sorted_products = sorted(productsList, key=lambda x: x['Category'])
