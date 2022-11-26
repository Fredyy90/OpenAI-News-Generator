from pprint import pprint
from wordpress import Wordpress
from articlegenerator import ArticleGenerator
from functions import *
from config import *
import pathlib
import openai
import sys

BASE_FOLDER = pathlib.Path(__file__).parent.resolve()
DATA_FILE = BASE_FOLDER / "data.json"
OUTPUT_FOLDER = BASE_FOLDER / "output"
IMAGE_FOLDER = BASE_FOLDER / "images"

wordpress = Wordpress(WORDPRESS_URL, WORDPRESS_USER, WORDPRESS_PASSWORD)
article_generator = ArticleGenerator(OPENAI_APIKEY)
data = loadJson(DATA_FILE)

def main():

    #wordpress.create_post("Test", "Test", "https://oaidalleapiprodscus.blob.core.windows.net/private/org-jLqSsHASKxBFeZXHXlBuebGX/user-NdbhHVSEauA5XAStUnGO7VXa/img-MvoJV2TNWRYkrHotu9owiNIg.png?st=2022-11-26T15%3A50%3A42Z&se=2022-11-26T17%3A50%3A42Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2022-11-26T01%3A46%3A32Z&ske=2022-11-27T01%3A46%3A32Z&sks=b&skv=2021-08-06&sig=VPr/UagKgAiCWnh8Mv/dnNB%2B1/Yg76tCBd71iZAJ1GA%3D")
    #sys.exit()

    feed = getSourceFeed()

    for entry in feed:
        if entry["guid"] not in data:

            print("Title: " + entry.title)
            print("Description: " + entry.description)

            newArticle = article_generator.generateArticle(entry.title, entry.description)

            output = {}
            output["old_title"] = entry.title
            output["old_description"] = entry.description
            output["new_title"] = newArticle["title"]
            output["new_description"] = newArticle["description"]
            output["new_image_url"] = newArticle["image"]

            wordpress.create_post(newArticle["title"], newArticle["description"], newArticle["image"])

            data[entry["guid"]] = output
            pprint(newArticle)
            saveJson(data, DATA_FILE)
            sys.exit()


if  __name__ ==  "__main__" :
    main()