import requests
import json

#r = requests.get("http://127.0.0.1:5000/table/list")

#data = {
# "collection": {
#         "data": [
#             {"name": "table_name", "value": "unicorns"}
#         ]
#     }
#}
#JSONData = json.dumps(data)
#r = requests.get("http://127.0.0.1:5000/table/showall", data=JSONData)

#print(r.content)

data = {
    "collection":  {
        "data":  [
            {"name": "table_name", "value": "unicorns"},
            {"name": "name", "value": "Jimbob"},
            {"name": "dob", "value": "1985,1,2,3,4"},
            {"name": "loves", "value": "long walks in the rain,french movies"},
            {"name": "weight", "value": 666},
            {"name": "gender", "value": "m"},
            {"name": "vampires", "value": 12}
        ]
    }
}

# data = {
#     "collection": {
#         "data": [
#             {"name": "table_name", "value": "players"},
#             {"name": "handle", "value": "Leeroy Jenkins"},
#             {"name": "first", "value": "Ben"},
#             {"name": "last", "value": "Schultz"},
#             {"name": "email", "value": "atleastihave@chicken.com"},
#             {"name": "passwd", "value": "raid"}
#         ]
#     }
# }
#
JSONData = json.dumps(data)
#r = requests.post("http://127.0.0.1:5000/table/post", data=JSONData)
r = requests.get("http://127.0.0.1:5000/table/post", data=JSONData)

print(r.content)

#data = {
#"collection": {
#        "data": [
#           {"name": "table_name", "value": "unicorns"},
#            {"name": "id_number", "value": "56e929263f7f7f52712efee9"}
#        ]
#    }
#}

#JSONData = json.dumps(data)

#r = requests.get("http://127.0.0.1:5000/table/showone/56e929263f7f7f52712efee9", data=JSONData)

#print(r.content)