# Source - https://stackoverflow.com/a/48131334
# Posted by Laxman, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-02, License - CC BY-SA 3.0

import csv
import json

file = 'contacts.csv'
json_file = 'originals.json'

#Read CSV File
def read_CSV(file, json_file):
    csv_rows = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        field = reader.fieldnames
        for row in reader:
            csv_rows.extend([{field[i]:row[field[i]] for i in range(len(field))}])
        convert_write_json(csv_rows, json_file)

#Convert csv data into json
def convert_write_json(data, json_file):
    with open(json_file, "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '), default=str)) #for pretty

def CSV_tuple(csvname):
    with open(csvname) as csvfile:
        reader = csv.reader(csvfile)
        csvdata = [tuple(row) for row in list(reader)[1:]]
    return csvdata

def JSON_tuple(jsonname):
    with open(jsonname) as f:
        data = json.load(f)
    tuples_list = [
        (r['first_name'], r['last_name'], r['email'], r['birthday'], r['group_id']) 
        for r in data
    ]

read_CSV(file,json_file)
