import re
import requests

from datetime import datetime
from bs4 import BeautifulSoup

IFB_BASE_URL = 'https://www.ifb.edu.br'


class Scraper:

    def start_requests(self, url):
        response = requests.get(url)
        response_soup = BeautifulSoup(response.text, 'html.parser')
        return self.get_news_list(response_soup)

    def get_news_list(self, response):
        news_list = []
        for news_item in response.find_all('div', class_='tileItem'):
            title, url = self.parse_title_and_url(item=news_item)
            image = self.parse_image(item=news_item)
            date_time = self.parse_datetime(item=news_item)
            description = self.parse_description(item=news_item)
            news_list.append({'title': title,
                              'datetime': date_time,
                              'description': description,
                              'image': image,
                              'url': url})
        news_list = sorted(news_list, key=lambda dict_: dict_['datetime'])
        return news_list

    @staticmethod
    def parse_title_and_url(item):
        title_content = item.find('h2', class_='tileHeadline')
        title = title_content.get_text().strip()
        url = IFB_BASE_URL + title_content.a.get('href')
        return title, url

    @staticmethod
    def parse_image(item):
        image_resource = item.find('img', class_='tileImage')
        image_src = IFB_BASE_URL + image_resource.get('src') if image_resource else ''
        return image_src

    @staticmethod
    def parse_datetime(item):
        datetime_content = item.find('div', class_='span2 tileInfo').get_text()
        datetime_match = re.search(r'(\d+/\d+/\d+\n\s\d+h\d+)', datetime_content)
        datetime_group = datetime_match.group() if datetime_match else ''
        datetime_object = datetime.strptime(datetime_group, '%d/%m/%y  %Hh%M').isoformat(' ', 'minutes')
        return datetime_object

    def parse_description(self, item):
        description_content = item.find('span', class_='description').get_text()
        description = self.__treat_text(text=description_content)
        return description

    @staticmethod
    def __treat_text(text):
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\t', ' ', text)
        text = re.sub(r'\r', ' ', text)
        text = re.sub(r'\xa0', ' ', text)
        text = re.sub(r'  +', ' ', text)
        return text.strip()


if __name__ == "__main__":
    scraper = Scraper()
