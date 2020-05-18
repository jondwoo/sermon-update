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

def getChannelResource(youtube):
    request = youtube.channels().list( # pylint: disable=maybe-no-member
        part="contentDetails",
        maxResults=config.maxResults,
        id="UCTFhNnaRpZTan-5K3yXWngw"
    )
    channel = request.execute()

    return channel

def getVideos(youtube, nlpc):
    videos = {}
    video_title = ''
    video_title_no_scripture = ''
    video_id = ''

    upload_list_id = nlpc['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    request = youtube.playlistItems().list( # pylint: disable=maybe-no-member
        part="snippet",
        maxResults=config.maxResults,
        playlistId=upload_list_id
    )
    uploads = request.execute()
    
    for video in uploads['items']:
        video_title = video['snippet']['title']
        split_str = video_title.split(' (', 1)
        video_title_no_scripture = split_str[0]

        video_id = video['snippet']['resourceId']['videoId']
        
        videos[video_title_no_scripture] = video_id
    
    return videos
