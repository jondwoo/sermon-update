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


    # '''
    # auto generate page with configured number of rows and columns
    # '''
    # print('Updating page...')
    # content = generatePage.generatePage()
    
    # if (generatePage.isGenerated(content)):
    #     generatePage.updatePage('sermon_page.html', content)
    #     print('done')
    # else:
    #     print(f"Missing fields for sermon ID: {content['_id']}")
    #     print(json.dumps(content, indent=2))