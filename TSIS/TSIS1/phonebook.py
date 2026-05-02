import csv, json
import connect
from config import load_config
from converter import convert_write_json, CSV_tuple, JSON_tuple

# region data
groups = ("Friends", "Family", "Work", "Other")

csvname = 'contacts.csv'
csvdata = CSV_tuple(csvname)
impjsonname = "originals.json"
jsondata = JSON_tuple(impjsonname)

expjsonname = "contacts.json"
# endregion

# execution
# connect.create_tables()

# for g in groups:
#    connect.insert_group(g)

# data = connect.select_contacts_dict()
# convert_write_json(data, expjsonname)

# connect.insert_contacts(csvdata)
# connect.insert_contacts(jsondata)