import sermon_info
import youtube
import json
import database
import datetime
import config
import generatePage



if __name__ == "__main__":

    '''
    grab sermon info from API and insert to DB
    '''
    print('updating database...')
    mydb = database.connectToDB()
    # database.deleteAll(mydb)  # for testing
    sermon_col = database.getSermonCollection(mydb)

    ## manual inserts
    sermon = sermon_info.getSermonInfo()
    curr_id, next_id, db_id = sermon_info.getPlanID_info()
    inserted = database.insertSermon(sermon_col, sermon, next_id, db_id)
    if inserted:
        # current ID updates on insert and points to upcoming sermon
        sermon_info.updateCurrID(next_id, db_id)
        database.getSermonList(sermon_col, config.limit_val)
    else: 
        database.getSermonList(sermon_col, config.limit_val)
    print('done')
    print('')

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


    ## update May 10th sermon title
    # sermon_col.update_one(
    #     {'_id': 18},
    #     {
    #         '$set' : {'sermon_title':'Living Hope in a Lost World'}
    #     }
    # )

    '''
    auto generate page with configured number of sermons
    '''
    print('updating page..')
    index_html = generatePage.generatePage()
    generatePage.writeToFile('sermon_page.html', index_html)
    print('done')