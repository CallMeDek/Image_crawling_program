from apscheduler.schedulers.background import BackgroundScheduler
from google_images_download import google_images_download   
import datetime
import time
import os
import sys


def main():
    if not (os.path.isfile("config_file.json")):
        print("There's no config_file... Please check.")
        sys.exit(0)

    response = google_images_download.googleimagesdownload()   
    arguments = {"config_file": "config_file.json"}   
    paths = response.download(arguments)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Done : {0}".format(now))


if __name__ == "__main__":
    main()
    scheduler = BackgroundScheduler()
    scheduler.add_job(main, 'interval', seconds=1, start_date="2020-03-17 11:05:00")
    scheduler.start()
    while True:
        time.sleep(0.3)