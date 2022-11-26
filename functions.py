import feedparser
import os
import json

RSS_FEED = "https://www.tagesschau.de/xml/rss2/"
def getSourceFeed(feedUrl = RSS_FEED):
    feed = feedparser.parse(feedUrl)
    return feed.entries


def saveJson(data, filename):

    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def loadJson(filename):
    if os.path.exists(filename) == False:
        return {}

    with open(filename) as json_file:
        data = json.load(json_file)
        return data