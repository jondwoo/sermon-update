import tokens
import pymongo
import sermon_info
import youtube
import json
from datetime import datetime


def connectToDB():
    client = pymongo.MongoClient(f'mongodb+srv://{tokens.USERNAME}:{tokens.PASS}@cluster0-fmo1o.mongodb.net/test?retryWrites=true&w=majority')
    db = client.nlpc
    
    return db

def getSermonCollection(db):
    return db.sermons

def insertSermon(col, sermon):
    # # check if video id exists for lastest sermon
    # sermon_title = sermon['sermon_title']
    # try:
        
    #     if videos[sermon_title.lower()] == None:
    #         sermon['youtube_id'] = ''
    #     else:
    #         video_id = videos[sermon_title.lower()]
    #         sermon['youtube_id'] = video_id
    # except AttributeError:
    #     print('Sermon title does not exist in PCO API')
    #     print('PCO API')
    #     print(json.dumps(sermon,indent=2))
    #     print('\nYOUTUBE API')
    #     print(json.dumps(videos,indent=2))
    
    col.insert_one(sermon)
    print(f"Inserted \"{sermon['sermon_title']}\"")

def deleteAll(db):
    db.sermons.delete_many({})

def findSermons(collection, limit_val):
    print(f'Retrieving last {limit_val} sermons')

    cursor = collection.find().sort('_id', pymongo.DESCENDING).limit(limit_val)
    for sermon in cursor:
        print(json.dumps(sermon, indent=2))