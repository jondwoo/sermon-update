import sermon_info
import youtube
import json
import database
import datetime
import config


if __name__ == "__main__":
    mydb = database.connectToDB()
    sermon_col = database.getSermonCollection(mydb)
    # database.deleteAll(mydb)  # for testing

    ## manual inserts
    sermon = sermon_info.getSermonInfo()
    curr_id, next_id, db_id = sermon_info.getPlanID_info()

    # current sermon points to this week's sermon
    if (sermon['youtube_id'] == ''):
        database.findSermons(sermon_col, config.limit_val)
    else:
        print(json.dumps(sermon,indent=2))
        database.insertSermon(sermon_col, sermon)
        sermon_info.updateCurrID(next_id, db_id)


    ## batch inserts
    # while(True):
        # sermon = sermon_info.getSermonInfo()
        # curr_id, next_id, db_id = sermon_info.getPlanID_info()

        # current id points to this week's sermon
        # if (sermon['youtube_id'] == ''):
        #   database.findSermons(sermon_col, config.limit_val)
        #   break
        # else:
        #     print(json.dumps(sermon,indent=2))
        #     database.insertSermon(sermon_col, sermon)
        #     sermon_info.updateCurrID(next_id, db_id)

   