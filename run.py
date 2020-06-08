import sermon_info
import youtube
import json
import database
import config
import generatePage

from datetime import datetime

if __name__ == "__main__":
    # database.deleteAll() # for testing

    # get sermon information and insert/update database
    while(True):
        print(f'Current date: {datetime.today().date()}')
        if database.isEmpty():
            # get first sermon
            print(f"Databases is empty. Retrieving first sermon information...")
            first_sermon_info = sermon_info.getSermonInfo('first')
            database.insertSermon(first_sermon_info)
        else:
            if sermon_info.isNewSunday():
                # insert new sermon
                new_sermon = sermon_info.getSermonInfo('new')
                database.insertSermon(new_sermon)
            else:
                # update previous sermons
                print(
                    f"No new sermons. Updating all previous incomplete sermon information...")
                print('')
                database.updateIncompleteSermons()
                break

    # auto generate page with configured number of rows and columns
    print('Updating page...')
    content = generatePage.generatePage()
    generatePage.updatePage(content)
