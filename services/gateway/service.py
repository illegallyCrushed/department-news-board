import http
from nameko.rpc import RpcProxy
from nameko.web.handlers import http

import json


class GatewayService:

    name = 'gateway_service'
    file_rpc = RpcProxy('file_service')
    search_rpc = RpcProxy('search_service')

    @http('GET', '/')
    def index(self, request):
        try:
            file_returns = self.file_rpc.helloworld()
        except Exception as e:
            file_returns = 'File Service Error: ' + str(e)

        try:
            search_returns = self.search_rpc.helloworld()
        except Exception as e:
            search_returns = 'Search Service Error: ' + str(e)

        return json.dumps({'file_returns': file_returns, 'search_returns': search_returns})
