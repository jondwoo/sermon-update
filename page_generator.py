import os
import database
import config
import datetime
from pprint import pprint


pageTemplatePath = "/templates/page-template.html"
sermonTemplatePath = "/templates/sermon-template.html"
sermonPagePath = "/sermon_page.html"


def get_file(filename):
    if os.path.isfile(filename):
        with open(filename) as f:
            return f.read()


def update_page(content):
    filename = os.getcwd() + sermonPagePath
    if os.path.isfile(filename):
        with open(filename, "w") as writer:
            for html in content:
                writer.write(html)
        print("done")


def is_generated(content):
    if isinstance(content, str):
        return True
    else:
        return False


def generate_page():
    sermonBody = []
    count = 0
    pageTemplate = get_file(os.getcwd() + pageTemplatePath)
    sermonTemplate = get_file(os.getcwd() + sermonTemplatePath)

    # retrieve sermons from database
    print(f"Retrieving last {config.limit_val} complete sermons...")
    recent_sermons = database.get_sermon_list(config.limit_val)

    sermonBody.append('<div class="row">')
    # replace HTML {{FIELD}} for every sermon
    for sermon in recent_sermons["data"]:
        formatted_date = (
            datetime.datetime.strptime(sermon["date"], "%Y-%m-%d")
            .date()
            .strftime("%B %d, %Y")
        )
        try:
            # at every config.col value, make a new row
            if count != config.col:
                sermonBody.append(
                    sermonTemplate.replace("{{YOUTUBEID}}", sermon["youtube_id"])
                    .replace("{{DATE}}", formatted_date)
                    .replace("{{TITLE}}", sermon["sermon_title"])
                    .replace("{{SPEAKER}}", sermon["speaker"])
                    .replace("{{SCRIPTURE}}", sermon["scripture"])
                )
                count += 1  # keep track of each card
            else:
                sermonBody.append("</div>")
                sermonBody.append('<div class="row">')
                sermonBody.append(
                    sermonTemplate.replace("{{YOUTUBEID}}", sermon["youtube_id"])
                    .replace("{{DATE}}", formatted_date)
                    .replace("{{TITLE}}", sermon["sermon_title"])
                    .replace("{{SPEAKER}}", sermon["speaker"])
                    .replace("{{SCRIPTURE}}", sermon["scripture"])
                )
                count = 1  # reset row
        except TypeError:
            print(f"Sermon for {sermon['sermon_title']} has type NULL in a field")

    # combine entire HTML element to one HTML element at index 0
    mergedSermonBody = ["".join(sermonBody[0:])]

    # generate and return the final page
    return pageTemplate.replace("{{SERMONS}}", mergedSermonBody[0])
