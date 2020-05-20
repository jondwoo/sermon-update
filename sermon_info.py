import requests
import json
import tokens
import csv
import youtube
import datetime


def isNewSermon(sermon_date, upload_date):
    print(sermon_date, upload_date)
    return sermon_date == upload_date

def getPlanID_info():
    curr_id = ''
    next_id = ''
    # id for db
    db_id = ''

    # get current ID
    with open('currentPlanID.csv', 'r') as file:
        reader = csv.reader(file, delimiter='=')
        for row in reader:
            if row[0] == 'curr_id':
                curr_id = row[1]
            if row[0] == 'db_id':
                db_id = row[1] 

    # get next ID
    plan_details_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{curr_id}/')
    r = requests.get(
        plan_details_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    next_id = body['data']['relationships']['next_plan']['data']['id']

    return curr_id, next_id, db_id
    
def getPlanDates(curr_id, next_id):
    sermon_date = ''
    next_sermon_date = ''

    # current sermon date
    plan_details_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{curr_id}/')
    r = requests.get(
        plan_details_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    sermon_date = body['data']['attributes']['dates']

    # next sermon date
    plan_details_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{next_id}/')
    r = requests.get(
        plan_details_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    next_sermon_date = body['data']['attributes']['dates']
    
    #return as date object
    sermon_date =  datetime.datetime.strptime(sermon_date, '%B %d, %Y').date()
    # .strftime('%Y-%m-%d')
    next_sermon_date =  datetime.datetime.strptime(next_sermon_date, '%B %d, %Y').date()
    # .strftime('%Y-%m-%d')
    return sermon_date, next_sermon_date

def getPlanTitle(curr_id):
    sermon_title = ''
    plan_items_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{curr_id}/items')
    r = requests.get(
        plan_items_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    for item in body['data']:
        if (item['attributes']['title'] == 'Preaching of the Word'):
            sermon_title = item['attributes']['description']  
    return sermon_title

def getPlanScripture(curr_id):
    scripture = ''
    plan_items_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{curr_id}/items')
    r = requests.get(
        plan_items_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    for item in body['data']:
        if (item['attributes']['title'] == 'Reading of the Word'):
            scripture = item['attributes']['description']
    return scripture

def getPlanSpeaker(curr_id):
    speaker = ''
    plan_team_members_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{curr_id}/team_members')
    r = requests.get(
        plan_team_members_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    for item in body['data']:
        if (item['attributes']['team_position_name'] == 'Preacher'):
            speaker = item['attributes']['name']
    return speaker

def getPlanSeries(curr_id):
    series_title = ''
    plan_details_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{curr_id}/')
    r = requests.get(
        plan_details_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    if body['data']['attributes']['series_title'] != None:
        series_title = body['data']['attributes']['series_title']
    return series_title

def updateCurrID(next_id, db_id):
    with open('currentPlanID.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter='=')
        writer.writerow(['curr_id', next_id])
        writer.writerow(['db_id', int(db_id)+1])

def getSermonInfo():
    # Jan 5, 2020: 40782442
    # May 3, 2020: 46963824

    ## PCO
    sermon_info = {}

    # plan_IDs[0] = current ID
    # plan_IDs[1] = next ID
    # plan_IDs[2] = db_id
    plan_IDs = getPlanID_info() 

    sermon_date, next_sermon_date = getPlanDates(plan_IDs[0], plan_IDs[1])
    sermon_title = getPlanTitle(plan_IDs[0])
    scripture = getPlanScripture(plan_IDs[0])
    speaker = getPlanSpeaker(plan_IDs[0])
    series_title = getPlanSeries(plan_IDs[0])

    # populate sermon with resources from PCO API
    sermon_info['_id'] = int(plan_IDs[2])
    sermon_info['series'] = series_title
    sermon_info['sermon_title'] = sermon_title
    sermon_info['scripture'] = scripture
    sermon_info['speaker'] = speaker
    sermon_info['date'] = sermon_date.strftime('%B %d, %Y')
    sermon_info['next_sermon_date'] = next_sermon_date.strftime('%Y-%m-%d')
    sermon_info['insert_date'] = datetime.date.today().strftime('%Y-%m-%d')
    sermon_info['plan_id'] = int(plan_IDs[0])
    sermon_info['youtube_id'] = ''

    ## YOUTUBE
    youtube_resource = youtube.authenticateYoutubeAPI()
    nlpc_resource = youtube.getChannelResource(youtube_resource)
    video_list = youtube.getVideos(youtube_resource, nlpc_resource)

    # populate sermon with youtube ID's from YOUTUBE API
    try:
        for video in video_list:
            # either sermon title or sermon date must match that of video title or upload date to assign its video id to that sermon
            if (video['title'].lower() == sermon_info['sermon_title'].lower() or
                    video['upload_date'] == sermon_date.strftime('%Y-%m-%d')):
                video_id = video['id']
                sermon_info['youtube_id'] = video_id
    except AttributeError:
        print('No sermon title in PCO API')
        # print(f"Cannot add video_id for \"{sermon_info['sermon_title']}\"")
    

    return sermon_info