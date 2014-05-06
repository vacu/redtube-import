# 0 - iframe
# 1 - thumbs ( , as split)
# 2 - title
# 3 - tag
# 4 - category
# 5 - pornstar
# 6 - duration

import csv
from pymongo import MongoClient

# mongo connection
client      = MongoClient()
# selecting database
db          = client.amateurxxx

# collections
categoriesC = db.categories
videosC     = db.videos

# read csv file
with open('YouPorn-Embed-Videos-Dump.csv', newline='', encoding='utf-8') as csvfile:
    videoReader = csv.reader(csvfile, delimiter='|', quoting=csv.QUOTE_NONE)

    for row in videoReader:
        isSaved = videosC.find_one({'title': row[2].rstrip()})

        if not isSaved:
            iframe = row[0]

            if row[0].startswith('"') and row[0].endswith('"'):
                iframe = str(row[0][1:-1])

            iframeParts = iframe.split('<br />')
            iframe = bytes(str(iframeParts[0].encode('utf-8')), 'ascii')

            thumbParts = row[1].split(',')
            thumb = thumbParts[0]

            if (thumbParts[0] == None):
                thumb = thumbParts[1]

            title = row[2].rstrip()
            if title.startswith('"') and title.endswith('"'):
                title = str(title[1:-1])

            videoElem = {
                'title'     : title,
                'images'    : thumb,
                'iframe'    : iframe,
                'views'     : 0,
                'likes'     : 0,
                'dislikes'  : 0
            }

            toReplace = [
                ",", "`", "'", "/", "!", "\"", "(", ")", "+", "&", "\\", "<", ">", ".", ";", ":",
                "?", "]", "[", "{", "}", "^", "%", "*", "$", "#", "@", "~", '-', '´'
            ]

            for character in toReplace:
                row[2] = row[2].replace(character, '')

            url = row[2].replace(" ", "-").lower()
            videoElem['url'] = url

            tags = ''
            if 4 < len(row) :
                tags = row[4]

            if tags.startswith('"') and tags.endswith('"'):
                tags = tags[1:-1]

            videoElem['keywords'] = tags
            videosC.save(videoElem)

print('Done!')
