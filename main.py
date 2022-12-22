from pprint import pprint
from wordpress import Wordpress
from articlegenerator import ArticleGenerator
from functions import *
from config import *
import pathlib
import sys

BASE_FOLDER = pathlib.Path(__file__).parent.resolve()
DATA_FILE = BASE_FOLDER / "data.json"
OUTPUT_FOLDER = BASE_FOLDER / "output"
IMAGE_FOLDER = BASE_FOLDER / "images"

wordpress = Wordpress(WORDPRESS_URL, WORDPRESS_USER, WORDPRESS_PASSWORD)
article_generator = ArticleGenerator(OPENAI_APIKEY)
data = loadJson(DATA_FILE)

def main():

    #wordpress.create_post("Test", "Test", "https://via.placeholder.com/300/09f/fff.png", tags=['Cara'], category='Kultur')
    #sys.exit()

    feed = getSourceFeed()

    for entry in feed:
        if entry["guid"] not in data:

            print("Title: " + entry.title)
            print("Description: " + entry.description)

            newArticle = article_generator.generateArticle(entry.title, entry.description, categories=wordpress.get_all_categories())

            output = {
                "old":{
                    "title": entry.title,
                    "description": entry.description
                },
                "new": newArticle
            }

            if ("title" in newArticle
                and "description" in newArticle
                and "image" in newArticle
                and "tags" in newArticle
                and "category" in newArticle):

                wordpress.create_post(newArticle["title"], newArticle["description"], newArticle["image"], tags=newArticle["tags"], category=newArticle["category"])

            data[entry["guid"]] = output
            pprint(output)
            saveJson(data, DATA_FILE)


if  __name__ ==  "__main__" :
    main()