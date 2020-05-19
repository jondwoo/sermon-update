import sermon_info
import youtube
import json
from datetime import datetime

if __name__ == "__main__":
    sermon_list = []
    while(True):
        # PCO
        sermons = {}

        curr_id = sermon_info.getCurrPlanID() 
        next_id, next_next_id = sermon_info.getNextIDs(curr_id)

        # get date and convert to datetime object for comparison
        sermon_date, next_sermon_date = sermon_info.getPlanDates(curr_id, next_id)
        sermon_date_obj = datetime.strptime(sermon_date, '%B %d, %Y').date()
        next_sermon_date_obj = datetime.strptime(next_sermon_date, '%B %d, %Y').date()

        sermon_title = sermon_info.getPlanTitle(curr_id)
        scripture = sermon_info.getPlanScripture(curr_id)
        speaker = sermon_info.getPlanSpeaker(curr_id)
        series_title = sermon_info.getPlanSeries(curr_id)

        print(f'Plan ID: {curr_id}')
        print(f'Date: {sermon_date}')
        print(f'Sermon Title: {sermon_title}')
        print(f'Scripture: {scripture}')
        print(f'Speaker: {speaker}')
        print(f'Series: {series_title}')

        # fill new sermon dict with each loop
        sermons['plan_id'] = curr_id
        sermons['date'] = sermon_date
        sermons['sermon_title'] = sermon_title
        sermons['scripture'] = scripture
        sermons['speaker'] = speaker
        sermons['series'] = series_title
        sermons['next_sermon_date'] = next_sermon_date_obj.strftime('%Y-%m-%d')
        sermons['todays_date'] = datetime.date(datetime.now()).strftime('%Y-%m-%d')

        sermon_list.append(sermons)

        # check if today is a new sunday (current plan's next date)
        isNextDate = sermon_info.compareDates(next_sermon_date_obj)
        if isNextDate:
            sermon_info.updateCurrID(next_id, next_next_id, curr_id)
        else:
            break

    print('SERMON LIST')
    print(json.dumps(sermon_list,indent=2))
    print('')

    # YOUTUBE
    youtube_resource = youtube.authenticateYoutubeAPI()
    nlpc_resource = youtube.getChannelResource(youtube_resource)
    videos = youtube.getVideos(youtube_resource, nlpc_resource)

    print('YOUTUBE')
    print(json.dumps(videos,indent=2))


# Jan 5, 2020: 40782442
# Apr 5, 2020: 46074866
