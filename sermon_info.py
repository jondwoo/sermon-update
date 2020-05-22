import requests
import json
import tokens
import csv
import youtube
import os
import database
from datetime import datetime
from datetime import timedelta


def getSermonSeries(id):
    series_title = ''
    plan_details_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{id}/')
    r = requests.get(
        plan_details_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    if body['data']['attributes']['series_title'] != None:
        series_title = body['data']['attributes']['series_title']
    return series_title


def getSermonTitle(id):
    try:
        plan_items_url = (
            f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{id}/items')
        r = requests.get(
            plan_items_url, 
            auth=(tokens.APP_ID, tokens.SECRET)
        )
        body = json.loads(r.text)

        for item in body['data']:
            if (item['attributes']['title'] == 'Preaching of the Word'):
                sermon_title = item['attributes']['description']

        return sermon_title
    except UnboundLocalError:
        print('No sermon title defined in PCO')
        return None


def getSermonScripture(id):
    try:
        plan_items_url = (
            f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{id}/items')
        r = requests.get(
            plan_items_url, 
            auth=(tokens.APP_ID, tokens.SECRET)
        )
        body = json.loads(r.text)

        for item in body['data']:
            if (item['attributes']['title'] == 'Reading of the Word'):
                scripture = item['attributes']['description']

        return scripture
    except UnboundLocalError:
        print('No scripture defined in PCO')
        return None


def getSermonSpeaker(id):
    try:
        plan_team_members_url = (
            f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{id}/team_members')
        r = requests.get(
            plan_team_members_url, 
            auth=(tokens.APP_ID, tokens.SECRET)
        )
        body = json.loads(r.text)

        for item in body['data']:
            if (item['attributes']['team_position_name'] == 'Preacher'):
                speaker = item['attributes']['name']

        return speaker
    except UnboundLocalError:
        print('No speaker defined in PCO')
        return None
    

def getSermonDate(id):
    try:
        plan_details_url = (
            f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{id}/')
        r = requests.get(
            plan_details_url, 
            auth=(tokens.APP_ID, tokens.SECRET)
        )
        body = json.loads(r.text)

        sermon_date = body['data']['attributes']['dates']
        #return as date object
        sermon_date =  datetime.strptime(sermon_date, '%B %d, %Y').date()
        return sermon_date
    except UnboundLocalError:
        print('No date defined in PCO')
        return None


def getSermonNextID(id):
    try:
        plan_details_url = (
            f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{id}/')
        r = requests.get(
            plan_details_url, 
            auth=(tokens.APP_ID, tokens.SECRET)
        )
        body = json.loads(r.text)

        next_id = body['data']['relationships']['next_plan']['data']['id']

        return next_id
    except UnboundLocalError:
        print('No next sermon ID defined in PCO')


def appendYoutubeID(sermon_title):
    ## YOUTUBE
    youtube_resource = youtube.authenticateYoutubeAPI()
    nlpc_resource = youtube.getChannelResource(youtube_resource)
    video_list = youtube.getVideos(youtube_resource, nlpc_resource)

    # populate sermon with youtube ID's from YOUTUBE API
    try:
        for video in video_list:
            if (video['title'].lower() == sermon_title.lower()):
                video_id = video['id']
                return video_id
    except AttributeError:
        print('Cannot link youtube ID - No sermon title in PCO')
        return None


def updateLastSermon(sermon):
    # grab latest id and re-populate the data
    sermon_info = {}
    sermon_info['series'] = getSermonSeries(sermon['plan_id'])
    sermon_info['sermon_title'] = getSermonTitle(sermon['plan_id'])
    sermon_info['scripture'] = getSermonScripture(sermon['plan_id'])
    sermon_info['speaker'] = getSermonSpeaker(sermon['plan_id'])
    # dates and id will never change
    sermon_info['date'] = sermon['date']
    sermon_info['plan_id'] = int(sermon['plan_id'])
    sermon_info['next_id'] = int(sermon['next_id'])
    sermon_info['youtube_id'] = appendYoutubeID(sermon_info['sermon_title'])

    return sermon_info


def getNewSermon(last_sermon):
    sermon_info = {}
    sermon_info['series'] = getSermonSeries(last_sermon['next_id'])
    sermon_info['sermon_title'] = getSermonTitle(last_sermon['next_id'])
    sermon_info['scripture'] = getSermonScripture(last_sermon['next_id'])
    sermon_info['speaker'] = getSermonSpeaker(last_sermon['next_id'])
    sermon_info['date'] = getSermonDate(last_sermon['next_id']).strftime('%Y-%m-%d')
    sermon_info['plan_id'] = int(last_sermon['next_id'])
    sermon_info['next_id'] = int(getSermonNextID(sermon_info['plan_id']))
    sermon_info['youtube_id'] = appendYoutubeID(sermon_info['sermon_title'])

    return sermon_info


def getFirstPlan():
    # get all plans
    plans_url = ('https://api.planningcenteronline.com/services/v2/service_types/764160/plans?offset=105/')
    r = requests.get(
        plans_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    first_sermon_info = {}
    plan_id = body['data'][0]['id']
    first_sermon_info['series'] = getSermonSeries(plan_id)
    first_sermon_info['sermon_title'] = getSermonTitle(plan_id)
    first_sermon_info['scripture'] = getSermonScripture(plan_id)
    first_sermon_info['speaker'] = getSermonSpeaker(plan_id)
    first_sermon_info['date'] = datetime.strptime(body['data'][0]['attributes']['dates'], '%B %d, %Y').strftime('%Y-%m-%d')
    first_sermon_info['plan_id'] = int(plan_id)
    first_sermon_info['next_id'] = int(getSermonNextID(plan_id))
    first_sermon_info['youtube_id'] = appendYoutubeID(first_sermon_info['sermon_title'])

    return first_sermon_info


def getSermonInfo():
    # check if empty database
    last_sermon = database.findMostRecent()
    if last_sermon != None:
        # if it is a new sunday, get new info, else update last sermon's info
        last_sermon_date_obj = datetime.strptime(last_sermon['date'], '%Y-%m-%d')
        today = datetime.today()

        # not a new sunday; update last sermon
        if today < (last_sermon_date_obj + timedelta(days=7)):
            print(f"No new sermons. Updating last sermon information for {last_sermon['date']}...")
            updated_sermon = updateLastSermon(last_sermon) 
            return updated_sermon
            
        # is a new sunday
        else:
            # get new sunday sermon's info based on last sermon's next id
            new_sunday_date = (last_sermon_date_obj + timedelta(days=7)).date()
            print(f"Retrieving sermon information for {new_sunday_date}...")
            new_sermon = getNewSermon(last_sermon)
            return new_sermon
            
    # is empty
    else:
        print(f"Databases is empty. Retrieving first sermon information...")
        first_sermon_info = getFirstPlan()
        return first_sermon_info
