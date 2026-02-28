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
# 3. Practice
# -----------------------

with open('Practice4/sample_data.json', "r") as file:
    data = json.load(file)

root = data["imdata"]
print("Interface Status\n"
"================================================================================\n"
"DN                                                 Description           Speed    MTU  \n"
"-------------------------------------------------- --------------------  ------  ------\n")

for datas in root:
    path = datas["l1PhysIf"]["attributes"]
    print(f"{path["dn"]:<50}", f"{path.get("descr"):<20}", "", f"{path["speed"]:<6}", "", f"{path["mtu"]:<6}")