
from messenger import Messenger
from scraper import Scraper

from utils.campuses import campuses_info


class Updater:
    """
        Initializes the miner to parse all campuses and
        send the news on their respective channels
    """

    file_path_updates = 'last_news_updates.json'

    def first_step(self):
        """ Gets the campuses information to retrieve the links for each one  """
        for campus_key, campus_value in campuses_info.items():
            campus_links = campus_value['links']
            self.parse_campus_links(campus_links=campus_links,
                                    campus_key=campus_key)

    def parse_campus_links(self, campus_links, campus_key):
        """ Gets the campus links and send them to the scraper to parse the data """
        for link_key, link_value in campus_links.items():
            news_list = Scraper().start_requests(url=link_value)
            self.parse_news_list(news_list=news_list,
                                 campus_key=campus_key,
                                 link_key=link_key)

    def parse_news_list(self, news_list, campus_key, link_key):
        """ Gets the campus news data and call the message updater  """
        for news in news_list:
            self.message_update(news=news,
                                campus_key=campus_key,
                                link_key=link_key)

    def message_update(self, news, campus_key, link_key):
        """ Update the news and forward it to your respective channel """
        messenger = Messenger(news=news,
                              campus_key=campus_key,
                              link_key=link_key,
                              file_path=self.file_path_updates)
        messenger.updates()


if __name__ == "__main__":
    updater = Updater()
    updater.first_step()
