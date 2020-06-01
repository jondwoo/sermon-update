import os
import re
import requests
import json
import csv
import tokens
import youtube
import database
import PCO
from datetime import datetime
from datetime import timedelta


def getSermonSeries(id):
    series_title = ''
    body = PCO.getPlanDetails(id)

    if body['data']['attributes']['series_title'] == '' or body['data']['attributes']['series_title'] == None:
        return ''
    else:
        series_title = body['data']['attributes']['series_title']
    return series_title


def getSermonTitle(id):
    try:
        body = PCO.getPlanItems(id)

        for item in body['data']:
            if (item['attributes']['title'] == 'Preaching of the Word'):
                # if blank or null return as None for query purposes
                if item['attributes']['description'] == '' or item['attributes']['description'] == None:
                    print('No sermon title defined in PCO')
                    return None

                # if guest speaker in string, only extract the title
                try:
                    substrings = re.search(r'(.*) \((.+?)\)', item['attributes']['description'])
                    return substrings.group(1)
                except AttributeError:
                    # no guest speaker in string
                    substrings = re.search(r'(.*)', item['attributes']['description'])
                    return substrings.group(0)

    except UnboundLocalError:
        print('No sermon title defined in PCO')
        # must return as None for query purposes
        return None


def getSermonScripture(id):
    try:
        body = PCO.getPlanItems(id)

        for item in body['data']:
            if (item['attributes']['title'] == 'Reading of the Word'):
                scripture = item['attributes']['description']
                # check if scripture is empty or null
                if item['attributes']['description'] == None or item['attributes']['description'] == '':
                    print('No scripture defined in PCO')
                    scripture =  ''
        return scripture
    except UnboundLocalError:
        print('No scripture defined in PCO')
        return ''


def getSermonSpeaker(id):
    speaker = ''
    try:
        body = PCO.getPlanTeamMembers(id)

        # no data available
        if body['data'] == []:
            print('Checking for speaker name in PCO sermon title...')
            if checkSermonTitleForSpeaker(id) == '':
                # if no speaker in sermon title, check series title
                print('Checking for speaker name in PCO series title...')
                if checkSeriesForSpeaker(id) == '':
                    # no speaker exists
                    print('No speaker defined in PCO')
                    speaker =  ''
                else:
                    speaker = checkSeriesForSpeaker(id)
            else:
                speaker = checkSermonTitleForSpeaker(id)
            return ''
        else:
            for item in body['data']:
                if (item['attributes']['team_position_name'] == 'Preacher'):
                    speaker = item['attributes']['name']
                    # if speaker is empty, check sermon title
                    if item['attributes']['name'] == None or item['attributes']['name'] == '':
                        print('Checking for speaker name in PCO sermon title...')
                        if checkSermonTitleForSpeaker(id) == '':
                            # if no speaker in sermon title, check series title
                            print('Checking for speaker name in PCO series title...')
                            if checkSeriesForSpeaker(id) == '':
                                # no speaker exists
                                print('No speaker defined in PCO')
                                speaker =  ''
                            else:
                                speaker = checkSeriesForSpeaker(id)
                        else:
                            speaker = checkSermonTitleForSpeaker(id)
                    return speaker
            # "Preacher" entry does not exist, check sermon title
            print('Checking for speaker name in PCO sermon title...')
            if checkSermonTitleForSpeaker(id) == '':
                # if no speaker in sermon title, check series title
                print('Checking for speaker name in PCO series title...')
                if checkSeriesForSpeaker(id) == '':
                    # no speaker exists
                    print('No speaker defined in PCO')
                    speaker =  ''
                else:
                    speaker = checkSeriesForSpeaker(id)
            else:
                speaker = checkSermonTitleForSpeaker(id)
            return speaker
    except UnboundLocalError:
        print('No speaker defined in PCO')
        return ''


def checkSermonTitleForSpeaker(id):
    try:
        body = PCO.getPlanItems(id)

        for item in body['data']:
            if (item['attributes']['title'] == 'Preaching of the Word'):
                # check if sermon title exists
                if item['attributes']['description'] == '' or item['attributes']['description'] == None:
                    return ''
                else:
                    # if sermon title not empty, check for guest speaker in string, only extract the speaker
                    try:
                        substrings = re.search(r'(.*) \((.+?)\)', item['attributes']['description'])
                        return substrings.group(2)  # guest speaker name
                    except AttributeError:
                        # no guest speaker in string
                        return ''

    except UnboundLocalError:
        print('No sermon title defined in PCO')
        # must return as None for query purposes
        return None


def checkSeriesForSpeaker(id):
    body = PCO.getPlanDetails(id)

    # check if series title exists
    if body['data']['attributes']['series_title'] == '' or body['data']['attributes']['series_title'] == None:
        return ''
    else:
        # check if [Guest Speaker] as the series title
        if body['data']['attributes']['series_title'] == '[Guest Speaker]':
            # check if guest speaker name is listed
            if body['data']['attributes']['title'] == '' or body['data']['attributes']['title'] == None:
                return ''
            else:
                return body['data']['attributes']['title']  # guest speaker name
        else:
            return ''


def getSermonDate(id):
    try:
        body = PCO.getPlanDetails(id)

        sermon_date = body['data']['attributes']['dates']
        #return as date object
        sermon_date =  datetime.strptime(sermon_date, '%B %d, %Y').date()
        return sermon_date
    except UnboundLocalError:
        print('No date defined in PCO')
        return None


def getSermonNextID(id):
    try:
        body = PCO.getPlanDetails(id)

        next_id = body['data']['relationships']['next_plan']['data']['id']

        return next_id
    except UnboundLocalError:
        print('No next sermon ID defined in PCO')
        return ''


def appendYoutubeID(sermon):
    ## YOUTUBE
    youtube_resource = youtube.authenticateYoutubeAPI()
    nlpc_resource = youtube.getChannelResource(youtube_resource)
    video_list = youtube.getVideos(youtube_resource, nlpc_resource)

    # populate sermon with youtube ID's from YOUTUBE API
    try:
        for video in video_list:
            if (video['title'].lower() == sermon['sermon_title'].lower() or
                video['upload_date'] == sermon['date']):
                video_id = video['id']
                return video_id
    except AttributeError:
        print('Cannot link youtube ID')
        return None


def updateSermonInformation(sermon):
    # grab latest id and re-populate the data
    sermon_info = {}
    sermon_info['series'] = getSermonSeries(sermon['plan_id'])
    sermon_info['sermon_title'] = getSermonTitle(sermon['plan_id'])
    sermon_info['scripture'] = getSermonScripture(sermon['plan_id'])
    sermon_info['speaker'] = getSermonSpeaker(sermon['plan_id'])
    sermon_info['date'] = getSermonDate(sermon['plan_id']).strftime('%Y-%m-%d')
    # IDs will never change
    sermon_info['plan_id'] = int(sermon['plan_id'])
    sermon_info['next_id'] = getSermonNextID(sermon['next_id'])
    sermon_info['youtube_id'] = appendYoutubeID(sermon_info)

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
    sermon_info['youtube_id'] = appendYoutubeID(sermon_info)

    return sermon_info


def getFirstPlan():
    # get all plans
    body = PCO.getPlanList()

    first_sermon_info = {}
    plan_id = body['data'][0]['id']
    first_sermon_info['series'] = getSermonSeries(plan_id)
    first_sermon_info['sermon_title'] = getSermonTitle(plan_id)
    first_sermon_info['scripture'] = getSermonScripture(plan_id)
    first_sermon_info['speaker'] = getSermonSpeaker(plan_id)
    first_sermon_info['date'] = datetime.strptime(body['data'][0]['attributes']['dates'], '%B %d, %Y').strftime('%Y-%m-%d')
    first_sermon_info['plan_id'] = int(plan_id)
    first_sermon_info['next_id'] = int(getSermonNextID(plan_id))
    first_sermon_info['youtube_id'] = appendYoutubeID(first_sermon_info)

    return first_sermon_info


def isNewSunday():
    last_sermon = database.findMostRecent()
    last_sermon_date_obj = datetime.strptime(last_sermon['date'], '%Y-%m-%d')
    today = datetime.today()
    if today < (last_sermon_date_obj + timedelta(days=7)):
        return False
    else:
        return True

def getSermonInfo(option):


    if option == 'first':
        first_sermon_info = getFirstPlan()
        return first_sermon_info

    elif option == 'new':
        # update last week's sermon first
        print('Updating previous sermon...')
        last_sermon = database.findMostRecent()
        updated_last_sermon = updateSermonInformation(last_sermon)

        today = datetime.today().strftime('%Y-%m-%d')
        updated_last_sermon = database.findMostRecent()
        updated_last_sermon_date_obj = datetime.strptime(updated_last_sermon['date'], '%Y-%m-%d')
        new_sunday_date = (updated_last_sermon_date_obj + timedelta(days=7)).date()

        print(f"Retrieving sermon information for {new_sunday_date}...")
        new_sermon = getNewSermon(updated_last_sermon)
        # check new sermon's date matches with today's date
        if today == new_sermon['date']:
            return new_sermon
        else:
            print(f"Sermon date not accurate. Retrieved sermon date {new_sermon['date']}")
            return new_sermon

