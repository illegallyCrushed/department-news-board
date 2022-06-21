from nameko.rpc import rpc

class NewsService:

    name = 'news_service'

    @rpc
    def get_all_news(self):
        pass

    @rpc
    def get_news_by_id(self, news_id):
        pass

    @rpc
    def add_new_news(self, title, content, datetime, publisher):
        pass

    @rpc
    def edit_news(self, news_id, title, content, datetime):
        pass

    @rpc
    def delete_news(self, news_id):
        pass

    