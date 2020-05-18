"""
Project Details:
  - list out past 6 sunday plans
    - sermon title
    - sermon series
    - date
    - preacher
"""
import requests
import json
import tokens

url = "https://api.planningcenteronline.com/services/v2/service_types/800507/plans?offset=94"
r = requests.get(url, auth=(tokens.APP_ID, tokens.SECRET))
data = json.loads(r.text)


def getSundayPlanIDs():
    id_list = []
    for i in data["data"]:
        id_list.append(i["id"])
        # if i["relationships"]["next_plan"]["data"] != None:
        #     print(json.dumps(i["relationships"]["next_plan"]["data"]["id"], indent=2))
    return id_list



