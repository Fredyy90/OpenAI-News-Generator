import feedparser
import os
import json
from config import *

def getSourceFeed(feedUrl = RSS_FEED):
    feed = feedparser.parse(feedUrl)
    return feed.entries


def saveJson(data, filename):

    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def loadJson(filename):
    if os.path.exists(filename) == False:
        return {}

    with open(filename) as json_file:
        data = json.load(json_file)
        return data