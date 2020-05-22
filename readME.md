## Video Sermon Auto Upload

Python script to automate NLPC's video sermon uploads<br><br>
Note:
* The plan ID starts from upcoming sermon 
* CSV file increments db_id and updates automatically with the latest plan ID after every insert
* ommitting "/watch?v=" in youtube_id
* only the first sermon of a series will have sermon['series'] populated

Requirements:
* Get personal token from PCO and api key from youtube API
    - `https://api.planningcenteronline.com/oauth/applications`
    - `https://developers.google.com/youtube/v3/docs`
* Check requirements.txt for python libraries

TODO:
* send alert for missing sermon fields
* keep plan status via plan date
* update web page with only valid video
* keep track of last week's sermon until 12pm this sunday (so db checks for updates on every run)