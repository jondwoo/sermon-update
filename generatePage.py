import os
import database
import config
import datetime


page_template_path = "/templates/page-template.html"
sermon_template_path = "/templates/sermon-template.html"


def generatePage():
    sermon_body = []
    sermon_row = []
    count = 0
    page_template = getFile(os.getcwd() + page_template_path)
    sermon_template = getFile(os.getcwd() + sermon_template_path)
    
    # retrieve sermons from database
    mydb = database.connectToDB()
    sermon_col = database.getSermonCollection(mydb)
    recent_sermons = database.getSermonList(sermon_col, config.limit_val)
    
    # replace {{FIELD}} for every sermon
    for sermon in recent_sermons['data']:
        formatted_date = datetime.datetime.strptime(sermon['date'], '%Y-%m-%d').date().strftime('%B %d, %Y')

        # add sermon to row
        sermon_row.append(
            sermon_template
                .replace('{{YOUTUBEID}}', sermon['youtube_id'])
                .replace('{{DATE}}', formatted_date)
                .replace('{{TITLE}}', sermon['sermon_title'])
                .replace('{{SPEAKER}}', sermon['speaker'])
                .replace('{{SCRIPTURE}}', sermon['scripture'])
        )
        count += 1 # keep track of each card
        
        # at every 3rd card, append to body and make a new row
        if count == 3:
            sermon_body.append('<div class=\"row\">')
            for index in range(len(sermon_row)):
                sermon_body.append(sermon_row[index])
            sermon_body.append('</div>')
            sermon_row = []
            count = 0
    
    # combine entire HTML element to one HTML element at index 0
    merged_sermon_body = [''.join(sermon_body[0:])]
    
    # generate final page
    final_page = page_template.replace('{{SERMONS}}', merged_sermon_body[0])
    return final_page


def getFile(filename):
    if os.path.isfile(filename):
        with open(filename) as f:
            return f.read()


def writeToFile(filename, content):
    with open(filename, 'w') as writer:
        for html in content:
            writer.write(html)


if __name__ == "__main__":
    index_html = generatePage()
    writeToFile('sermon_page.html', index_html)
