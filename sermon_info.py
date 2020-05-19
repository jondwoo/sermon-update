import requests
import json
import tokens
import csv
from datetime import datetime


def compareDates(next_sermon_date):
    today = datetime.date(datetime.now())
    print(f'Next Sermon\'s Date: {next_sermon_date}')
    print(f'Today\'s Date: {today}')
    print('')
    return (next_sermon_date <= today)

def getCurrPlanID():
    with open('currPlanID.csv', 'r') as file:
        reader = csv.reader(file, delimiter='=')
        for row in reader:
            if row[0] == 'curr_id':
                return row[1]  # return the value of curr_id

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

def getNextIDs(curr_id):
    next_id = ''
    next_next_id = ''

    # get next ID
    plan_details_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{curr_id}/')
    r = requests.get(
        plan_details_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    next_id = body['data']['relationships']['next_plan']['data']['id']

    # get next next ID
    plan_details_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{next_id}/')
    r = requests.get(
        plan_details_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    next_next_id = body['data']['relationships']['next_plan']['data']['id']
    return next_id, next_next_id

def updateCurrID(next_id, next_next_id, curr_id):
    with open('currPlanID.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter='=')
        writer.writerow(['curr_id', next_id])
        writer.writerow(['next_id', next_next_id])
        writer.writerow(['prev_id', curr_id])
