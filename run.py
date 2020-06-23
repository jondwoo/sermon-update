import sermon_info
import youtube
import json
import database
import config
import page_generator

from datetime import datetime

if __name__ == "__main__":
    # database.deleteAll() # for testing

    # get sermon information and insert/update database
    while True:
        print(f"Current date: {datetime.today().date()}")
        if database.is_empty():
            # get first sermon
            print(f"Databases is empty. Retrieving first sermon information...")
            initialSermonInfo = sermon_info.get_sermon(True)
            database.insert_sermon(initialSermonInfo)
        else:
            if sermon_info.is_new_sunday():
                # insert new sermon
                newSermon = sermon_info.get_sermon(False)
                database.insert_sermon(newSermon)
            else:
                # update previous sermons
                print(
                    f"No new sermons. Updating all previous incomplete sermon information..."
                )
                print("")
                database.update_incomplete_sermons()
                break

    # auto generate page with configured number of rows and columns
    print("Updating page...")
    content = page_generator.generate_page()
    page_generator.update_page(content)
