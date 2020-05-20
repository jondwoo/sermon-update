import tokens
import pymongo
import sermon_info
import youtube
import json
import config
from datetime import datetime


def connectToDB():
    client = pymongo.MongoClient(f'mongodb+srv://{tokens.USERNAME}:{tokens.PASS}@cluster0-fmo1o.mongodb.net/test?retryWrites=true&w=majority')
    db = client.nlpc
    
    return db

def getSermonCollection(db):
    return db.sermons

def insertSermon(col, sermon, next_id, db_id):
    # returns true and false flag for while loop
    if (sermon['youtube_id'] == ''):
        print(f"No sermon video available for {sermon['date']}")
        return False
    else:
        print(json.dumps(sermon,indent=2))
        col.insert_one(sermon)
        print(f"Inserted \"{sermon['sermon_title']}\"")
        return True
        
def deleteAll(db):
    db.sermons.delete_many({})

def getSermonList(collection, limit_val):
    sermon_dict = {}
    sermon_list = []
    print(f'Retrieving last {limit_val} sermons')
    cursor = collection.find().sort('_id', pymongo.DESCENDING).limit(limit_val)
    sermon_dict['data'] = sermon_list
    for sermon in cursor:
        sermon_list.append(sermon)

    print(json.dumps(sermon_dict, indent=2))
    # return sermon_dict