from flask import Flask, request, jsonify
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
# Database details
client = MongoClient()
db = client.FantasyDB


# Equivalent to:
# "SHOW TABLES"
# Receives a list table request
# Returns a JSON object list of all the tables in the database
@app.route('/table/list', methods=['GET'])
def listTable():

    result = db.collection_names()
    itemList = []

    for row in result:
        name = {"data": [{"name": "tableName", "value": row}]}
        itemList.append(name)
#
    JSONDictionary = {"version": "1.0",
                      "href": request.base_url,
                      "Items": itemList
                          }

    return jsonify(collection=JSONDictionary)


# Equivalent to:
# "SELECT * FROM tablename"
# Receives a table name
# Returns all of its entries along with their URLs
@app.route('/table/showall', methods=['GET'])
def selectAllFrom():

    tableName = None
    itemList = []
    jsonData = json.loads(request.get_data().decode("utf-8"))
    data = jsonData["collection"]["data"]
    for c in data:
        if c["name"] == "table_name":
            tableName = c["value"]

    if tableName:

        result = db[tableName].find()

        for row in result:
            row["_id"] = str(row["_id"])

            item = {"href": request.url_root + "table/showone/" + str(row["_id"]), "data": row}
            itemList.append(item)


        JSONDictionary = {"version": "1.0",
                          "href": request.base_url,
                          "Items": itemList
                          }

        return jsonify(collection=JSONDictionary)


# Equivalent to:
# "INSERT INTO tableName VALUES data"
# Writes entries to a table
# Returns a series of links
@app.route('/table/post', methods=['GET', 'POST'])
def insert():

    tableName = None
    jsonData = json.loads(request.get_data().decode("utf-8"))
    data = jsonData["collection"]["data"]

    # Here lieth the POST section, dealing with write requests
    if request.method == 'POST':

        for c in data:

            if c["name"] == "table_name":
                tableName = c["value"]

        if tableName:
            number = ""
            numberList = []
            i = len(data[2]["value"])
            for n in data[2]["value"]:
                i -= 1

                if "," in n:
                    numberList.append(number)
                    number = ""
                elif i == 0:
                    number += n
                    numberList.append(number)
                else:
                    number += n


            like = "'"
            i = len(data[3]["value"])
            for l in data[3]["value"]:
                i -= 1

                if "," in l:
                    like += "'"
                    like += l
                elif i == 0:
                    like += l
                    like == "'"
                else:
                    like += l

            numberList.reverse()

            stuff = {
                    "name" : data[1]["value"],
                    "dob" : datetime(int(numberList.pop()), int(numberList.pop()), int(numberList.pop()), int(numberList.pop()), int(numberList.pop())),
                    "loves" : [like],
                    "weight" : data[4]["value"],
                    "gender" : data[5]["value"],
                    "vampires" : data[6]["value"]
            }
            db[tableName].insert(stuff)

            JSONDictionary = {"version": "1.0",
                                  "href": request.base_url,
                                  "Items": [],
                                  "links": [{"name": request.url_root + "table/showall/", "methods": ["Get"]},
                                            {"name": request.url_root + "table/showone/<itemId>", "methods": ["Get"]}]
                                  }

            return jsonify(collection=JSONDictionary)


    # Here lieth the GET section, dealing with describing specific tables
    else:
        for c in data:
            if c["name"] == "table_name":
                tableName = c["value"]



        if tableName:
            result = db[tableName].find_one()
            dataList = []
            for key in result:
                dataList.append({"name": key, "value": ""})

            JSONDictionary = {"version": "1.0",
                              "href": request.base_url,
                              "Items": [],
                              "links": [{"name": request.url_root + "table/showall/", "methods": ["Get"]},
                                {"name": request.url_root + "table/post/", "methods": ["Get", "Post"]}],
                              "template": {"data": dataList}
                              }

            return jsonify(collection=JSONDictionary)


# Equivalent to:
# "SELECT * FROM " tableName "WHERE ID=idNum"
# Shows an individual entry from a table
# Returns a series of links, along with the entry
@app.route('/table/showone/<itemId>', methods=['GET'])
def selectOneFrom(itemId):

    tableName = None
    itemList = []
    idNumber = itemId
    jsonData = json.loads(request.get_data().decode("utf-8"))
    data = jsonData["collection"]["data"]

    for c in data:
        if c["name"] == "table_name":
            tableName = c["value"]

    if tableName:
        result = db[tableName].find({"_id": ObjectId(idNumber)})

        for row in result:
            row["_id"] = str(row["_id"])

            item = {"href": request.url, "data": row}
            itemList.append(item)

        JSONDictionary = {"version": "1.0",
                          "Items": itemList,
                          "links": [{"name": request.url_root + "table/showall/", "methods": ["Get"]},
                                    {"name": request.url_root + "table/post/", "methods": ["Get", "Post"]}]
                          }

    return jsonify(collection=JSONDictionary)


if __name__ == '__main__':
    app.run()
