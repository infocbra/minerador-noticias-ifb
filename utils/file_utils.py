import json
import requests

from PIL import Image


class FileUtils:

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path) as json_file:
            return json.load(json_file)

    def write(self, last_news_dict):
        with open(self.file_path, 'w') as json_file:
            json_string = json.dumps(last_news_dict)
            json_file.write(json_string)

    def save_image(self, image_url):
        response = requests.get(image_url)
        with open(self.file_path, 'wb') as f:
            f.write(response.content)
            f.close()
        self.resize_image()
        return self.file_path

    def resize_image(self):
        image = Image.open(self.file_path)
        image.thumbnail((500, 500))
        image.save(self.file_path)
