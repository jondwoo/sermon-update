import os
import re
import requests
import json
import csv
import tokens
import database
import PCO
import youtube
from datetime import datetime
from datetime import timedelta


def get_sermon_series(id):
    seriesTitle = ""
    body = PCO.get_plan_details(id)

    if (
        body["data"]["attributes"]["series_title"] == ""
        or body["data"]["attributes"]["series_title"] == None
    ):
        return ""
    else:
        seriesTitle = body["data"]["attributes"]["series_title"]
    return seriesTitle


def get_sermon_title(id):
    try:
        body = PCO.get_plan_items(id)

        for item in body["data"]:
            if item["attributes"]["title"] == "Preaching of the Word":
                # if blank or null return as None for query purposes
                if (
                    item["attributes"]["description"] == ""
                    or item["attributes"]["description"] == None
                ):
                    print("No sermon title defined in PCO")
                    return None

                # if guest speaker in string, only extract the title
                try:
                    substrings = re.search(
                        r"(.*) \((.+?)\)", item["attributes"]["description"]
                    )
                    return substrings.group(1)
                except AttributeError:
                    # no guest speaker in string
                    substrings = re.search(r"(.*)", item["attributes"]["description"])
                    return substrings.group(0)

    except UnboundLocalError:
        print("No sermon title defined in PCO")
        # must return as None for query purposes
        return None


def get_sermon_scriptures(id):
    try:
        body = PCO.get_plan_items(id)

        for item in body["data"]:
            if item["attributes"]["title"] == "Reading of the Word":
                scripture = item["attributes"]["description"]
                # check if scripture is empty or null
                if (
                    item["attributes"]["description"] == None
                    or item["attributes"]["description"] == ""
                ):
                    print("No scripture defined in PCO")
                    scripture = ""
        return scripture
    except UnboundLocalError:
        print("No scripture defined in PCO")
        return ""


def get_sermon_speaker(id):
    speaker = ""
    try:
        body = PCO.get_plan_team_members(id)

        # no data available
        if body["data"] == []:
            print("Checking for speaker name in PCO sermon title...")
            if check_pco_sermon_title_for_speaker(id) == "":
                # if no speaker in sermon title, check series title
                print("Checking for speaker name in PCO series title...")
                if check_pco_series_for_speaker(id) == "":
                    # no speaker exists
                    print("No speaker defined in PCO")
                    speaker = ""
                else:
                    speaker = check_pco_series_for_speaker(id)
            else:
                speaker = check_pco_sermon_title_for_speaker(id)
            return ""
        else:
            for item in body["data"]:
                if item["attributes"]["team_position_name"] == "Preacher":
                    speaker = item["attributes"]["name"]
                    # if speaker is empty, check sermon title
                    if (
                        item["attributes"]["name"] == None
                        or item["attributes"]["name"] == ""
                    ):
                        print("Checking for speaker name in PCO sermon title...")
                        if check_pco_sermon_title_for_speaker(id) == "":
                            # if no speaker in sermon title, check series title
                            print("Checking for speaker name in PCO series title...")
                            if check_pco_series_for_speaker(id) == "":
                                # no speaker exists
                                print("No speaker defined in PCO")
                                speaker = ""
                            else:
                                speaker = check_pco_series_for_speaker(id)
                        else:
                            speaker = check_pco_sermon_title_for_speaker(id)
                    return speaker
            # "Preacher" entry does not exist, check sermon title
            print("Checking for speaker name in PCO sermon title...")
            if check_pco_sermon_title_for_speaker(id) == "":
                # if no speaker in sermon title, check series title
                print("Checking for speaker name in PCO series title...")
                if check_pco_series_for_speaker(id) == "":
                    # no speaker exists
                    print("No speaker defined in PCO")
                    speaker = ""
                else:
                    speaker = check_pco_series_for_speaker(id)
            else:
                speaker = check_pco_sermon_title_for_speaker(id)
            return speaker
    except UnboundLocalError:
        print("No speaker defined in PCO")
        return ""


def check_pco_sermon_title_for_speaker(id):
    try:
        body = PCO.get_plan_items(id)

        for item in body["data"]:
            if item["attributes"]["title"] == "Preaching of the Word":
                # check if sermon title exists
                if (
                    item["attributes"]["description"] == ""
                    or item["attributes"]["description"] == None
                ):
                    return ""
                else:
                    # if sermon title not empty, check for guest speaker in string, only extract the speaker
                    try:
                        substrings = re.search(
                            r"(.*) \((.+?)\)", item["attributes"]["description"]
                        )
                        return substrings.group(2)  # guest speaker name
                    except AttributeError:
                        # no guest speaker in string
                        return ""

    except UnboundLocalError:
        print("No sermon title defined in PCO")
        # must return as None for query purposes
        return None


def check_pco_series_for_speaker(id):
    body = PCO.get_plan_details(id)

    # check if series title exists
    if (
        body["data"]["attributes"]["series_title"] == ""
        or body["data"]["attributes"]["series_title"] == None
    ):
        return ""
    else:
        # check if [Guest Speaker] as the series title
        if body["data"]["attributes"]["series_title"] == "[Guest Speaker]":
            # check if guest speaker name is listed
            if (
                body["data"]["attributes"]["title"] == ""
                or body["data"]["attributes"]["title"] == None
            ):
                return ""
            else:
                return body["data"]["attributes"]["title"]  # guest speaker name
        else:
            return ""


def get_sermon_date(id):
    try:
        body = PCO.get_plan_details(id)

        sermon_date = body["data"]["attributes"]["dates"]
        # return as date object
        sermon_date = datetime.strptime(sermon_date, "%B %d, %Y").date()
        return sermon_date
    except UnboundLocalError:
        print("No date defined in PCO")
        return None


def get_sermon_next_id(id):
    try:
        body = PCO.get_plan_details(id)

        next_id = body["data"]["relationships"]["next_plan"]["data"]["id"]

        return next_id
    except UnboundLocalError:
        print("No next sermon ID defined in PCO")
        return ""


def append_youtube_id(sermon):
    ## YOUTUBE
    youtubeResource = youtube.authenticateYoutubeAPI()
    nlpcResource = youtube.getChannelResource(youtubeResource)
    videoList = youtube.getVideos(youtubeResource, nlpcResource)

    # populate sermon with youtube ID's from YOUTUBE API
    try:
        for video in videoList:
            if (
                video["title"].lower() == sermon["sermon_title"].lower()
                or video["upload_date"] == sermon["date"]
            ):
                videoId = video["id"]
                return videoId
    except AttributeError:
        print("Cannot link youtube ID")
        return None


def repopulate_current_sermon_info(currentSermon):
    # get latest id and re-populate the data
    updatedCurrentSermon = {}
    updatedCurrentSermon["series"] = get_sermon_series(currentSermon["plan_id"])
    updatedCurrentSermon["sermon_title"] = get_sermon_title(currentSermon["plan_id"])
    updatedCurrentSermon["scripture"] = get_sermon_scriptures(currentSermon["plan_id"])
    updatedCurrentSermon["speaker"] = get_sermon_speaker(currentSermon["plan_id"])
    updatedCurrentSermon["date"] = get_sermon_date(currentSermon["plan_id"]).strftime(
        "%Y-%m-%d"
    )
    updatedCurrentSermon["plan_id"] = int(currentSermon["plan_id"])
    updatedCurrentSermon["next_id"] = int(get_sermon_next_id(currentSermon["next_id"]))
    updatedCurrentSermon["youtube_id"] = append_youtube_id(currentSermon)

    return updatedCurrentSermon


# populate obj with the following weeks info
def populate_new_sermon_info(currentSermon):
    newSermon = {}
    newSermon["series"] = get_sermon_series(currentSermon["next_id"])
    newSermon["sermon_title"] = get_sermon_title(currentSermon["next_id"])
    newSermon["scripture"] = get_sermon_scriptures(currentSermon["next_id"])
    newSermon["speaker"] = get_sermon_speaker(currentSermon["next_id"])
    newSermon["date"] = get_sermon_date(currentSermon["next_id"]).strftime("%Y-%m-%d")
    newSermon["plan_id"] = int(currentSermon["next_id"])
    newSermon["next_id"] = int(get_sermon_next_id(newSermon["plan_id"]))
    newSermon["youtube_id"] = append_youtube_id(newSermon)

    return newSermon


def get_initial_sermon_info():
    # get all plans
    body = PCO.get_plan_list()

    initialSermon = {}
    plan_id = body["data"][0]["id"]
    initialSermon["series"] = get_sermon_series(plan_id)
    initialSermon["sermon_title"] = get_sermon_title(plan_id)
    initialSermon["scripture"] = get_sermon_scriptures(plan_id)
    initialSermon["speaker"] = get_sermon_speaker(plan_id)
    initialSermon["date"] = datetime.strptime(
        body["data"][0]["attributes"]["dates"], "%B %d, %Y"
    ).strftime("%Y-%m-%d")
    initialSermon["plan_id"] = int(plan_id)
    initialSermon["next_id"] = int(get_sermon_next_id(plan_id))
    initialSermon["youtube_id"] = append_youtube_id(initialSermon)

    return initialSermon


def is_new_sunday():
    currentSermon = database.find_most_recent().next()
    currentSermonDateObj = datetime.strptime(currentSermon["date"], "%Y-%m-%d")
    today = datetime.today()
    if today < (currentSermonDateObj + timedelta(days=7)):
        return False
    return True


def get_new_sermon(isInitial=False):

    if isInitial:
        initialSermon = get_initial_sermon_info()
        return initialSermon
    else:
        today = datetime.today().strftime("%Y-%m-%d")
        currentSermon = database.find_most_recent().next()

        currentSermonDateObj = datetime.strptime(currentSermon["date"], "%Y-%m-%d")
        newSundayDate = (currentSermonDateObj + timedelta(days=7)).date()

        print(f"Retrieving sermon information for {newSundayDate}...")
        newSermon = populate_new_sermon_info(currentSermon)
        # check new sermon's date matches with today's date
        if today == newSermon["date"]:
            return newSermon
        else:
            print(
                f"Sermon date not accurate. Retrieved sermon date {newSermon['date']}"
            )
            return newSermon

