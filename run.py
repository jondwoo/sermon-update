import plans
import youtube
from datetime import datetime

if __name__ == "__main__":
    while(True):
        curr_id = plans.getCurrPlanID()
        next_id, next_next_id = plans.getNextIDs(curr_id)

        sermon_date, next_sermon_date = plans.getPlanDates(curr_id, next_id)
        sermon_date_obj = datetime.strptime(sermon_date, '%B %d, %Y').date()
        next_sermon_date_obj = datetime.strptime(next_sermon_date, '%B %d, %Y').date()

        sermon_title = plans.getPlanTitle(curr_id)
        scripture = plans.getPlanScripture(curr_id)
        speaker = plans.getPlanSpeaker(curr_id)
        series_title = plans.getPlanSeries(curr_id)

        print(f'Plan ID: {curr_id}')
        print(f'Date: {sermon_date}')
        print(f'Sermon Title: {sermon_title}')
        print(f'Scripture: {scripture}')
        print(f'Speaker: {speaker}')
        print(f'Series: {series_title}')

        # if current plan's next date <= today, keep looping
        isNextDate = plans.compareDates(next_sermon_date_obj)
        if isNextDate:
            pass
        else:
            break

        plans.updateCurrID(next_id, next_next_id, curr_id)

        

# Jan 5, 2020: 40782442
# Apr 5, 2020: 46074866
