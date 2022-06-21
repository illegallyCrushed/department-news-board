from nameko.rpc import rpc

class UserService:

    name = 'user_service'

    @rpc
    def add_user(self, username, password):
        pass

    @rpc
    def check_password(self, username, password):
        pass

