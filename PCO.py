import requests
import tokens
import json

def getPlanList():
    plans_url = ('https://api.planningcenteronline.com/services/v2/service_types/764160/plans?offset=105/')
    r = requests.get(
        plans_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    return body

def getPlanDetails(id):
    plan_details_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{id}/')
    r = requests.get(
        plan_details_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
        )
    body = json.loads(r.text)

    return body

def getPlanItems(id):
    plan_items_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{id}/items')
    r = requests.get(
        plan_items_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
    )
    body = json.loads(r.text)

    return body

def getPlanTeamMembers(id):
    plan_team_members_url = (
        f'https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{id}/team_members')
    r = requests.get(
        plan_team_members_url, 
        auth=(tokens.APP_ID, tokens.SECRET)
    )
    body = json.loads(r.text)

    return body