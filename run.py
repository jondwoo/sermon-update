import sermon_info
import youtube
import json
import database
import datetime
import config
import generatePage



if __name__ == "__main__":

    '''
    retrieve sermon info from API and insert to DB
    '''
    print('Updating database...')
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
    #         break


    '''
    auto generate page with configured number of rows and columns
    '''
    print('Updating page...')
    content = generatePage.generatePage()
    
    if (generatePage.isGenerated(content)):
        generatePage.updatePage('sermon_page.html', content)
        print('done')
    else:
        print(f"Missing fields for sermon ID: {content['_id']}")
        print(json.dumps(content, indent=2))