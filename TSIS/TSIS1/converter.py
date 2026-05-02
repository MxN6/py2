import csv
import json


def read_csv_rows(csvname):
    with open(csvname, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def write_json(data, json_file):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=False, indent=4, separators=(',', ': '), default=str)


def load_json(jsonname):
    with open(jsonname, encoding='utf-8') as f:
        return json.load(f)
