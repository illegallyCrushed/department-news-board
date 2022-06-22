import http
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
import json


class GatewayService:

    name = 'gateway_service'
    file_rpc = RpcProxy('file_service')
    news_rpc = RpcProxy('news_service')
    user_rpc = RpcProxy('user_service')

    # user methods

    @http('POST', '/register')
    def register(self, request):
        pass

    @http('POST', '/login')
    def login(self, request):
        pass

    @http('DELETE', '/logout')
    def logout(self, request):
        pass

    # news methods

    @http('GET', '/news')
    def get_news(self, request):
        pass

    @http('GET', '/news/<int:news_id>')
    def get_news_by_id(self, request, news_id):
        pass

    @http('POST', '/news/post')
    def post_news(self, request):
        pass

    @http('PUT', '/news/<int:news_id>')
    def edit_news(self, request, news_id):
        pass

    @http('DELETE', '/news/<int:news_id>')
    def delete_news(self, request, news_id):
        pass

    # file methods

    @http('GET', '/file/<int:news_id>')
    def get_file(self, request, file_name):
        pass
