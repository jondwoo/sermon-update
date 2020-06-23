import sermon_info
import youtube
import json
import database
import config
import page_generator

from datetime import datetime

if __name__ == "__main__":
    # get sermon information and insert/update database
    while True:
        print(f"Current date: {datetime.today().date()}")
        if database.is_empty():
            # get first sermon
            print(f"Databases is empty. Retrieving first sermon information...")
            initialSermonInfo = sermon_info.get_new_sermon()
            database.insert_sermon(initialSermonInfo)
        else:
            if sermon_info.is_new_sunday():
                # update last week's sermon first
                print("Updating previous sermon...")
                currentSermonCursor = database.find_most_recent()
                database.update_sermon(currentSermonCursor)

                # insert new sermon
                newSermon = sermon_info.get_new_sermon()
                database.insert_sermon(newSermon)
            else:
                # update previous sermons
                print(
                    f"No new sermons. Updating all previous incomplete sermon information..."
                )
                print("")
                incompleteSermonCursor = database.get_incomplete_sermons()
                database.update_sermon(incompleteSermonCursor)
                break

    # auto generate page with configured number of rows and columns
    print("Updating page...")
    content = page_generator.generate_page()
    page_generator.update_page(content)
