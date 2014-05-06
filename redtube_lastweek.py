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
with open('a1eb5c9051960d57a32174f41a0f22171c579871.csv', newline='', encoding='utf-8') as csvfile:
    videoReader = csv.reader(csvfile, delimiter='|', quoting=csv.QUOTE_NONE)

    for row in videoReader:
        # 0 = ID
        # 1 = EMBED
        # 2 = THUMB
        # 3 = TITLE
        # 4 = CHANNEL

        isSaved = videosC.find_one({'title': row[3].rstrip()})

        if not isSaved:
            iframe = bytes(row[1], 'ascii')

            videoElem = {
                'title'     : row[3].rstrip(),
                'images'    : row[2],
                'iframe'    : iframe,
                'views'     : 0,
                'likes'     : 0,
                'dislikes'  : 0
            }

            toReplace = [
                ",", "`", "'", "/", "!", "\"", "(", ")", "+", "&", "\\", "<", ">", ".", ";", ":",
                "?", "]", "[", "{", "}", "^", "%", "*", "$", "#", "@", "~", '-'
            ]

            for character in toReplace:
                row[3] = row[3].replace(character, '')

            url = row[3].replace(" ", "-").lower()
            videoElem['url'] = url

            keywords = ''

            for newTag in row[4].split(';'):
                if keywords == '':
                    keywords = newTag.lower()
                else:
                    keywords += ',' + newTag.lower()

            videoElem['keywords'] = keywords
            videosC.save(videoElem)

print('Done')

