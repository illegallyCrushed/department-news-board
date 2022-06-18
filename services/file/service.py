from nameko.rpc import rpc


class FileService:

    name = 'file_service'

    @rpc
    def helloworld(self):
        return 'Hello World!'
