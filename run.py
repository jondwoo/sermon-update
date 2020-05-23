import sermon_info
import youtube
import json
import database
import config
import generatePage

from datetime import datetime
# import optparse

# parser = optparse.OptionParser()
# parser.add_option('-u', '--update',
#     action="store", dest="update",
#     help="update database", default="run")
# options, args = parser.parse_args()

if __name__ == "__main__":
    # retrieve sermon info from API and insert to DB
    database.deleteAll()  # for testing
    # if options.update:
    #     date = options.update
    #     field = input('Which field would you like to update?\n'
    #                 + '1. Series\n'
    #                 + '2. Sermon Title\n'
    #                 + '3. Scripture\n'
    #                 + '4. Speaker\n'
    #                 + '5. Youtube ID\n'
    #                 + 'q. Quit\n')

    #     # input validation here
    #     if field == 'q':
    #         exit(0)

    #     # input validation here
    #     value = input('Enter new value: ')
    #     database.findByDate(date, field, value)

    #     repeat = input('Update more sermons? y/n\n')
    #     if repeat == 'y':
    #         continue
    #     else:
    #         break
    # else:

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
