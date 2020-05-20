## Video Sermon Auto Upload

Python script to automate NLPC's video sermon uploads<br><br>
Note:
* The plan ID starts from upcoming sermon 
* CSV file increments db_id and updates automatically with the latest plan ID after every insert
* ommitting "/watch?v=" in youtube_id

Dependencies:
* Get personal token from PCO and api key from youtube API
    - `https://api.planningcenteronline.com/oauth/applications`
    - `https://developers.google.com/youtube/v3/docs`
* Check requirements.txt for python libraries

TODO:
* update null values for existing sermons

