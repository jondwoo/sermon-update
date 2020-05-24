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
    print('')

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


def updateIncompleteSermons():
    # retrieve all sermons with any null or '' values
    cursor = col.find({ "$or": [
        {'sermon_title': {'$in':[None, '']}}, 
        {'scripture': {'$in': [None, '']}},
        {'speaker': {'$in': [None, '' ]}},
        {'date': {'$in': [ None, '']}},
        { 'youtube_id': {'$in': [None, '']}}
        ] }).sort('date', pymongo.DESCENDING)
    

    for incomplete_sermon in cursor:
        print(f"Updating \"{incomplete_sermon['sermon_title']}\" for {incomplete_sermon['date']}...")
        updated_sermon = sermon_info.updateSermonInformation(incomplete_sermon)
        # pprint(updated_sermon)
        # break

        my_query = {'date': updated_sermon['date']}
        new_values = {'$set': {
            'series': updated_sermon['series'],
            'sermon_title': updated_sermon['sermon_title'],
            'scripture': updated_sermon['scripture'],
            'speaker': updated_sermon['speaker'],
            'date': updated_sermon['date'],
            'youtube_id': updated_sermon['youtube_id']
            }}
        col.update_one(my_query, new_values)

        # get updated sermon
        cursor = col.find({'_id': incomplete_sermon['_id']})
        # compare with old sermon
        for sermon in cursor:
            if str(incomplete_sermon) == str(sermon):
                print(f"Nothing to update")
            else:
                print(f"Updated")
        print('')


def isEmpty():
    last_sermon = findMostRecent()
    if last_sermon == None:
        return True
    else:
        return False


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