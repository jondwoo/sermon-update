# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import tokens
import json
import config

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


def authenticateYoutubeAPI():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = tokens.KEY

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    
    return youtube

def getChannelResource(channel):
    request = youtube.channels().list( # pylint: disable=maybe-no-member
        part="contentDetails",
        maxResults=config.maxResults,
        id="UCTFhNnaRpZTan-5K3yXWngw"
    )
    channel = request.execute()

    for item in channel['items']:
        print(json.dumps(item,indent=2))

if __name__ == "__main__":
    youtube = authenticateYoutubeAPI()
    getChannelResource(youtube)



