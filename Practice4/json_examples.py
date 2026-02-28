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