from nameko.rpc import rpc


class FileService:

    name = 'file_service'

    @rpc
    def get_file(self, news_id):
        pass

    @rpc
    def post_file(self, news_id, file_content):
        pass

    @rpc
    def delete_file(self, news_id):
        pass
