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
with open('export_online_mthumb_.csv', newline='', encoding='utf-8') as csvfile:
    videoReader = csv.reader(csvfile, delimiter='|', quoting=csv.QUOTE_NONE)

    for row in videoReader:
        print(row[0])
        # 0 = video id
        # 1 = thumb
        # 2 = url
        # 3 = title
        # 4 = channel
        # 5 = tag
        # 6 = pornstar
        # 7 = duration
        # 8 = date
        isSaved = videosC.find_one({'title': row[3].rstrip()})

        if not isSaved:
            iframe = '<object height="480" width="640"><param name="allowfullscreen" value="true">'
            iframe += '<param name="AllowScriptAccess" value="always"><param name="movie" value="http://embed.redtube.com/player/?id='+row[0]+'&style=redtube">'
            iframe += '<param name="FlashVars" value="id='+row[0]+'&style=redtube&autostart=false">'
            iframe += '<embed src="http://embed.redtube.com/player/?id='+row[0]+'&style=redtube" '
            iframe += 'allowfullscreen="true" AllowScriptAccess="always" flashvars="autostart=false" '
            iframe += 'pluginspage="http://www.adobe.com/shockwave/download/download.cgi?P1_Prod_Version=ShockwaveFlash" '
            iframe += 'type="application/x-shockwave-flash" height="480" width="640" />'
            iframe += '</object>'

            iframe = bytes(iframe, 'ascii')

            videoElem = {
                'title'     : row[3].rstrip(),
                'images'    : row[1],
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
