import requests
import tokens
import json


def get_plan_list():
    url = "https://api.planningcenteronline.com/services/v2/service_types/764160/plans?offset=105/"
    return _call_pco(url)


def get_plan_details(id):
    url = f"https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{id}/"
    return _call_pco(url)


def get_plan_items(id):
    url = f"https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{id}/items"
    return _call_pco(url)


def get_plan_team_members(id):
    url = f"https://api.planningcenteronline.com/services/v2/service_types/764160/plans/{id}/team_members"
    return _call_pco(url)


def _call_pco(url):
    r = requests.get(url, auth=(tokens.APP_ID, tokens.SECRET))
    if r.status_code == 200:
        return json.loads(r.text)
    return None
