from nameko.rpc import rpc
from dependencies.database import DatabaseProvider

class NewsService:

    name = 'news_service'
    database = DatabaseProvider()

    @rpc
    def get_all_news(self):
        return self.database.get_all_news()

    @rpc
    def get_news_by_id(self, news_id):
        return self.database.get_news_by_id(news_id)

    @rpc
    def add_new_news(self, title, content, unix, publisher):
        return self.database.add_new_news(title, content, unix, publisher)

    @rpc
    def check_news_id_exist(self, news_id):
        return len(self.database.get_news_by_id(news_id)) > 0

    @rpc
    def edit_news(self, news_id, title, content, unix):
        self.database.update_news(news_id, title, content, unix)

    @rpc
    def delete_news(self, news_id):
        self.database.delete_news(news_id)
    