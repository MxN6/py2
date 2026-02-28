import json

# -----------------------
# 1. Convert Python to JSON
# -----------------------

data = {
    "name": "Alice",
    "age": 25,
    "is_student": False
}

json_string = json.dumps(data, indent=4)
print("JSON String:")
print(json_string)


# -----------------------
# 2. Parse JSON
# -----------------------

parsed_data = json.loads(json_string)
print("Parsed Name:", parsed_data["name"])


# -----------------------
# 3. Write JSON to File
# -----------------------

with open("output.json", "w") as file:
    json.dump(data, file, indent=4)

print("JSON written to output.json")


# -----------------------
# 4. Read JSON File
# -----------------------

with open("output.json", "r") as file:
    loaded_data = json.load(file)

print("Loaded from file:", loaded_data)


# -----------------------
# 5. Working with sample-data.json
# -----------------------

# Make sure sample-data.json exists in the same folder
try:
    with open("sample-data.json", "r") as file:
        sample_data = json.load(file)

    print("Sample Data Loaded:")
    print(sample_data)

except FileNotFoundError:
    print("sample-data.json not found. Add it to test this part.")