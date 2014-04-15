import csv, re
from pymongo import MongoClient

# mongo connection
client      = MongoClient()
# selecting database
db          = client.amateurxxx

# collections
categoriesC = db.categories
videosC     = db.videos

# read csv file
with open('export_offline.csv', newline='', encoding='utf-8') as csvfile:
    videoReader = csv.reader(csvfile, delimiter='|', quoting=csv.QUOTE_NONE)

    for row in videoReader:
        # 0 = video id

        videos = videosC.find({})
        for video in videos:
            iframe = video['iframe'].decode('ascii')

            if row[0] in iframe:
                videosC.remove(video)

print('Done')
