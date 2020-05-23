import tokens
import pymongo
import sermon_info
import json
import config
from datetime import datetime
from pprint import pprint


client = pymongo.MongoClient(f'mongodb+srv://{tokens.USERNAME}:{tokens.PASS}@cluster0-fmo1o.mongodb.net/test?retryWrites=true&w=majority')
db = client.nlpc
col = db.sermons


def getSermonCollection():
    return db.sermons


def insertSermon(sermon): 
    # insert as new document
    print(json.dumps(sermon,indent=2))
    col.insert_one(sermon)
    print(f"Inserted \"{sermon['sermon_title']}\"")
    return True
        

def deleteAll():
    db.sermons.delete_many({})


def getSermonList(limit_val):
    sermon_dict = {}
    sermon_list = []
    
    # query for entries that are NOT null in these fields
    # i.e retrieve entries as long as it has sermon title, date, and youtube ID
    cursor = col.find({
        "sermon_title": {'$ne': None},
        # "scripture": {'$ne': None},
        # "speaker": {'$ne': None},
        "date": {'$ne': None},
        "youtube_id": {'$ne': None},
        }).sort('date', pymongo.DESCENDING).limit(limit_val)
    sermon_dict['data'] = sermon_list
    for sermon in cursor:
        sermon_list.append(sermon)

    # pprint(sermon_dict)
    return sermon_dict


def findMostRecent():
    # check if collection has at least one document
    cursor = db.sermons.find().sort('date', pymongo.DESCENDING).limit(1)
    for sermon in cursor:
        return sermon


def documentExists(sermon):
    cursor = db.sermons.find_one({"date": sermon['date']})
    if (isinstance(cursor, dict)):
        return True
    else:
        return False


def updateSermon(sermon):
    # update sermon info
    my_query = { 'date': sermon['date'] }
    new_values = { '$set': {
        'series': sermon['series'],
        'sermon_title': sermon['sermon_title'],
        'scripture': sermon['scripture'],
        'speaker': sermon['speaker'],
        'youtube_id': sermon['youtube_id']
        } }
    col.update_one(my_query, new_values)
    print(f"Updated \"{sermon['sermon_title']}\"")
    return True


# def findByDate(date, field, value):
#     my_query = { 'date': date }

#     if field == '1':
#         new_value = {'$set': {'series': value}}
#     elif field == '2':
#         new_value = {'$set': {'sermon_title': value}}
#     elif field == '3':
#         new_value = {'$set': {'scripture': value}}
#     elif field == '4':
#         new_value = {'$set': {'speaker': value}}
#     else:
#         new_value = {'$set': {'youtube_id': value}}
    
#     col.update_one(my_query, new_value)
#     print(f"Updated sermon for {date}")