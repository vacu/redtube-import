import csv, re
from pymongo import MongoClient

# mongo connection
client      = MongoClient()
# selecting database
db          = client.amateurxxx

# collections
categoriesC = db.categories
videosC     = db.videos

cnt = 1;

# read csv file
with open('deleted_videos.csv', newline='', encoding='utf-8') as csvfile:
    videoReader = csv.reader(csvfile, delimiter=' ', quoting=csv.QUOTE_NONE)

    for row in videoReader:
        # 0 - link
        videos = videosC.find({})

        for video in videos:
            iframe = video['iframe'].decode('ascii')

            if row[0] in str(iframe):
                print('Found')
                videosC.remove(video)
        print(cnt)
        cnt += 1

print('Done')
