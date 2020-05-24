import sermon_info
import youtube
import json
import database
import config
import generatePage

from datetime import datetime

if __name__ == "__main__":
    # get sermon information and insert/update database
    while(True):
        print(f'Current date: {datetime.today().date()}')
        sermon = sermon_info.getSermonInfo()
        if database.documentExists(sermon):
            database.updateSermon(sermon)
            break
        else:
            database.insertSermon(sermon)
        print('')

    # auto generate page with configured number of rows and columns
    print('Updating page...')
    content = generatePage.generatePage()
    generatePage.updatePage('sermon_page.html', content)
