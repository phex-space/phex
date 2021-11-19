class AuthenticationResult(object):
    def __init__(self, access_token: str, decoded_token: dict):
        self.__access_token = access_token
        self.__user = decoded_token

    @property
    def access_token(self):
        return self.__access_token

    @property
    def user(self):
        return self.__user
