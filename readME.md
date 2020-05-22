## Video Sermon Auto Upload

Python script to automate NLPC's video sermon uploads<br><br>
Note: 
* ommitting "/watch?v=" in youtube_id
* only the first sermon of a series will have sermon['series'] populated

Requirements:
* Get personal token from PCO and api key from youtube API
    - `https://api.planningcenteronline.com/oauth/applications`
    - `https://developers.google.com/youtube/v3/docs`
* Check requirements.txt for python libraries

TODO:
* send alert for missing sermon fields
* update web page with only valid video