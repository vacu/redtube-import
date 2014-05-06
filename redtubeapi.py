import urllib.request, json, base64
from pymongo        import MongoClient
from bson.objectid  import ObjectId

toReplace = [
    ",", "`", "'", "/", "!", "\"", "(", ")", "+", "&", "\\", "<", ">", ".", ";", ":",
    "?", "]", "[", "{", "}", "^", "%", "*", "$", "#", "@", "~"
]

# mongo connection
client      = MongoClient()
# selecting database
db          = client.amateurxxx

# collections
categoriesC = db.categories
videosC     = db.videos

# populate categories collection
categoryUrl     = 'http://api.redtube.com/?data=redtube.Categories.getCategoriesList&output=json'
categoryRes     = urllib.request.urlopen(categoryUrl).read().decode('utf-8')
categoryJson    = json.loads(categoryRes)
ctgErr          = False

if ctgErr == False:
    if 'code' in categoryJson:
        if categoryJson['code'] == 1005:
            ctgErr = True
            break
    else:
        for category in categoryJson['categories']:
            dbCategory = categoriesC.find_one({'url': category['category']})
            if not dbCategory:
                ctgElem = {
                    'title' : category['category'],
                    'url'   : category['category'],
                    'views' : 0
                }
                categoriesC.insert(ctgElem)


# populate videos based on category
categories = categoriesC.find({})
for category in categories:
    page = 1
    error = False

    if error == False:
        while page > 0:
            videoUrl    = 'http://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&category='+ category['url'] +'&page=' + str(page)
            videoRes    = urllib.request.urlopen(videoUrl).read().decode('utf-8')
            videoJson   = json.loads(videoRes)

            if 'code' in videoJson:
                if videoJson['code'] == 2001:
                    error = True
                    break
            else:
                for video in videoJson['videos']:
                    videoQuery = videosC.find_one({'title': video['video']['title']})
                    if not videoQuery:
                        videoElem = {
                            'title'     : video['video']['title'],
                            'images'    : video['video']['thumb'],
                            'views'     : video['video']['views'],
                            'likes'     : 0,
                            'dislikes'  : 0
                        }

                        for character in toReplace:
                            video['video']['title'] = video['video']['title'].replace(character, "")

                        videoElem['url'] = video['video']['title'].replace(" ", "-").lower()

                        tags = []

                        for tag in video['video']['tags']:
                            tags.append(tag['tag_name'].lower())

                        keywords = ''

                        for newTag in tags:
                            if keywords == '':
                                keywords = newTag
                            else:
                                keywords += ',' + newTag

                        videoElem['keywords'] = keywords

                        # Single video embed code
                        embedUrl    = 'http://api.redtube.com/?data=redtube.Videos.getVideoEmbedCode&video_id=' + video['video']['video_id'] + '&output=json'
                        embedRes    = urllib.request.urlopen(embedUrl).read().decode('utf-8')
                        embedJson   = json.loads(embedRes)
                        htmlPlayer  = base64.b64decode(embedJson['embed']['code'])
                        htmlPlayer  = str(htmlPlayer).replace('344', '480').replace('434', '640')

                        htmlPlayer  = bytes(htmlPlayer, 'ascii')
                        videoElem['iframe'] = htmlPlayer

                        # save new video in mongo
                        videosC.save(videoElem)

            page += 1

print('Done')
