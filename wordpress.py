import requests
import base64
import mimetypes
import os
from urllib.parse import urlparse

class Wordpress:

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.header = {'Authorization': 'Basic ' + base64.b64encode((username + ":" + password).encode()).decode('utf-8')}

    def create_media(self, file_path):
        if os.path.exists(file_path) == False:
            rsrc = requests.get(file_path) # try to download the image from the url
            if rsrc.status_code == 200:
                file_name = urlparse(file_path).path.split('/')[-1]
                file_type = mimetypes.guess_type(file_name)[0]
                file_data = rsrc.content
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

    def create_post(self, title, content, image_path = None, categories = None, tags = None):

        data = {
            'title' : title,
            'status': 'publish',
            'content':  content,
        }

        if(image_path != None):
            media = self.create_media(image_path)
            if(media != None):
                data["featured_media"] = media["id"]

        if(categories):
            data['categories'] = categories
        if(tags):
            data['tags'] = tags

        response = requests.post(self.url + '/wp-json/wp/v2/posts', headers=self.header, json=data)

        if(response.status_code == 201):
            return response.json()
        else:
            return None