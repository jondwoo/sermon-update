import sermon_info
import youtube
import json
import database
import datetime
import config


if __name__ == "__main__":
    mydb = database.connectToDB()
    # database.deleteAll(mydb)  # for testing
    sermon_col = database.getSermonCollection(mydb)

    # ## manual inserts
    sermon = sermon_info.getSermonInfo()
    curr_id, next_id, db_id = sermon_info.getPlanID_info()
    inserted = database.insertSermon(sermon_col, sermon, next_id, db_id)
    if inserted:
        # current ID updates on insert and points to upcoming sermon
        sermon_info.updateCurrID(next_id, db_id)
        database.getSermonList(sermon_col, config.limit_val)
    else: 
        database.getSermonList(sermon_col, config.limit_val)

    ## batch inserts
    # while(True):
    #     sermon = sermon_info.getSermonInfo()
    #     curr_id, next_id, db_id = sermon_info.getPlanID_info()
    #     inserted = database.insertSermon(sermon_col, sermon, next_id, db_id)
    #     if inserted:
    #         # current ID updates on insert and points to upcoming sermon
    #         sermon_info.updateCurrID(next_id, db_id)
    #     else:
    #         database.getSermonList(sermon_col, config.limit_val)
    #         break


   