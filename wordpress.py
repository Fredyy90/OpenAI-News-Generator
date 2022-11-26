import requests
import base64
import mimetypes
import os
from urllib.parse import urlparse

class Wordpress:

    tags = {}
    categories = {}

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.header = {'Authorization': 'Basic ' + base64.b64encode((username + ":" + password).encode()).decode('utf-8')}
        self.get_all_categories()

    def create_media(self, file_path):
        if os.path.exists(file_path) == False:
            rsrc = requests.get(file_path) # try to download the image from the url
            if rsrc.status_code == 200:
                file_name = urlparse(file_path).path.split('/')[-1]
                file_type = mimetypes.guess_type(file_name)[0]
                file_data = rsrc.content
            else:
                return None
        else:
            file_name = os.path.basename(file_path)
            file_type = mimetypes.guess_type(file_name)[0]
            file_data = open(file_path, 'rb').read()

        files = {
            'title' : file_name,
            'status': 'publish',
            'content':  file_name,
            'file': (file_name, file_data, file_type)
        }


        response = requests.post(self.url + '/wp-json/wp/v2/media', headers=self.header, files=files)

        if(response.status_code == 201):
            return response.json()
        else:
            return None

    def get_all_categories(self):

        if len(self.categories) > 0:
            return self.categories

        response = requests.get(self.url + '/wp-json/wp/v2/categories', headers=self.header)
        if(response.status_code == 200):
            data = response.json()
            for category in data:
                self.categories[category["id"]] = category["name"]
            return self.categories
        else:
            return None

    def get_all_tags(self):
        response = requests.get(self.url + '/wp-json/wp/v2/tags', headers=self.header)
        if(response.status_code == 200):
            data = response.json()
            for tag in data:
                self.tags[tag["id"]] = tag["name"]
            return data
        else:
            return None

    def create_tag(self, name):
        data = {
            'name' : name,
            'status': 'publish',
        }

        response = requests.post(self.url + '/wp-json/wp/v2/tags', headers=self.header, json=data)

        if(response.status_code == 201):
            data = response.json()
            self.tags[data["id"]] = data["name"]
            return data
        else:
            return None

    def create_post(self, title, content, image_path = None, category = None, tags = None):

        data = {
            'title' : title,
            'status': 'publish',
            'content':  content,
        }

        if(image_path != None):
            media = self.create_media(image_path)
            if(media != None):
                data["featured_media"] = media["id"]

        if(category):
            data['categories'] = []
            if(category in self.categories.values()):
                data['categories'].append(list(self.categories.keys())[list(self.categories.values()).index(category)])
        if(tags):
            data['tags'] = []
            for tag in tags:
                if(tag in self.tags.values()):
                    data['tags'].append(list(self.tags.keys())[list(self.tags.values()).index(tag)])
                else:
                    new_tag = self.create_tag(tag)
                    if(new_tag != None):
                        data['tags'].append(new_tag["id"])

        response = requests.post(self.url + '/wp-json/wp/v2/posts', headers=self.header, json=data)

        if(response.status_code == 201):
            return response.json()
        else:
            #print(response.text)
            return None