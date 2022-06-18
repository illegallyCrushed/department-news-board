from nameko.rpc import rpc

class SearchService:

    name = 'search_service'

    @rpc
    def helloworld(self):
        return 'Hello World!'
