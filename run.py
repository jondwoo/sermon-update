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
    # database.deleteAll(mydb)  # for testing

    print('Updating database...')
    sermon = sermon_info.getSermonInfo()
    database.insertSermon(sermon)
    print('')


    '''
    auto generate page with configured number of rows and columns
    '''
    print('Updating page...')
    content = generatePage.generatePage()
    generatePage.updatePage('sermon_page.html', content)