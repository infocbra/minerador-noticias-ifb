import telebot

from time import sleep

from telebot.apihelper import ApiException

from bot_auth_token import token

from utils.file_utils import FileUtils
from utils.campuses import campuses_info


class Messenger:

    bot = telebot.TeleBot(token['auth_token'])

    def __init__(self, news, campus_key, link_key, file_path):
        self.news = news
        self.campus_key = campus_key
        self.link_key = link_key
        self.file_path = file_path

    def updates(self):
        last_news_updates = FileUtils(file_path=self.file_path).read()
        update_date = last_news_updates[self.campus_key][self.link_key]
        if self.news['datetime'] > update_date:
            self.send_message()
            self.update_last_date(last_news_updates)
        sleep(1)

    def update_last_date(self, last_news_updates):
        object_dict = last_news_updates.get(self.campus_key)
        object_dict.update({self.link_key: self.news.get('datetime')})
        last_news_updates.update({self.campus_key: object_dict})
        FileUtils(file_path=self.file_path).write(last_news_dict=last_news_updates)

    def send_message(self):
        channel_id = campuses_info[self.campus_key]['channel']
        image = self.news.get('image')
        title = self.news.get('title')
        url = self.news.get('url')
        if image:
            try:
                self.bot.send_photo(chat_id=channel_id,
                                    photo=image,
                                    caption=f"\n*{title}*\nSaiba mais: {url}",
                                    parse_mode="markdown")
            except ApiException:
                image_file = FileUtils(file_path='utils/temp.jpg').save_image(image)
                with open(image_file, 'rb') as image:
                    self.bot.send_photo(chat_id=channel_id,
                                        photo=image.read(),
                                        caption=f"\n*{title}*\nSaiba mais: {url}",
                                        parse_mode="markdown")
        else:
            self.bot.send_message(chat_id=channel_id,
                                  text=f"\n*{title}* \n\nSaiba mais: {url}\n",
                                  parse_mode="markdown",
                                  disable_web_page_preview=True)
