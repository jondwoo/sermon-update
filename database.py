import tokens
import pymongo
import sermon_info
import json
import config
from datetime import datetime
from pprint import pprint


client = pymongo.MongoClient(
    f"mongodb+srv://{tokens.USERNAME}:{tokens.PASS}@cluster0.fmo1o.gcp.mongodb.net/{tokens.DBNAME}?retryWrites=true&w=majority"
)
db = client.nlpc
col = db.sermons


def get_sermon_collection():
    return db.sermons


def insert_sermon(sermon):
    # insert as new document
    print(json.dumps(sermon, indent=2))
    col.insert_one(sermon)
    print(f"Inserted \"{sermon['sermon_title']}\"")
    print("")

    return True


def delete_all():
    db.sermons.delete_many({})


def get_sermon_list(limit_val):
    sermonDict = {}
    sermonList = []

    # query for entries that are NOT null in these fields
    # i.e retrieve entries as long as it has sermon title, date, and youtube ID
    cursor = (
        col.find(
            {
                "sermon_title": {"$ne": None},
                "date": {"$ne": None},
                "youtube_id": {"$ne": None},
            }
        )
        .sort("date", pymongo.DESCENDING)
        .limit(limit_val)
    )
    sermonDict["data"] = sermonList
    for sermon in cursor:
        sermonList.append(sermon)

    return sermonDict


def find_most_recent():
    # check if collection has at least one document
    cursor = db.sermons.find().sort("date", pymongo.DESCENDING).limit(1)
    return cursor


def get_incomplete_sermons():
    # retrieve all sermons with any null or '' values
    cursor = col.find(
        {
            "$or": [
                {"sermon_title": {"$in": [None, ""]}},
                {"scripture": {"$in": [None, ""]}},
                {"speaker": {"$in": [None, ""]}},
                {"date": {"$in": [None, ""]}},
                {"youtube_id": {"$in": [None, ""]}},
            ]
        }
    ).sort("date", pymongo.DESCENDING)
    return cursor


def is_empty():
    cursor = find_most_recent()
    if cursor.next() == None:
        return True
    else:
        return False


def update_sermon(cursor):
    if cursor.count() == 0:
        print("No Sermons. Nothing to update")
    else:
        for sermon in cursor:
            print(f"Updating \"{sermon['sermon_title']}\" for {sermon['date']}...")
            updatedSermon = sermon_info.repopulate_current_sermon_info(sermon)

            myQuery = {"date": sermon["date"]}
            newValues = {
                "$set": {
                    "series": updatedSermon["series"],
                    "sermon_title": updatedSermon["sermon_title"],
                    "scripture": updatedSermon["scripture"],
                    "speaker": updatedSermon["speaker"],
                    "date": updatedSermon["date"],
                    "youtube_id": updatedSermon["youtube_id"],
                }
            }
            col.update_one(myQuery, newValues)

            # get updated sermon
            cursor = col.find({"_id": sermon["_id"]})

            # compare with old sermon
            if str(sermon) == str(cursor.next()):
                print(f"Nothing to update")
            else:
                print(f"Updated")
            print("")

    currentSermon = find_most_recent().next()
    return currentSermon
