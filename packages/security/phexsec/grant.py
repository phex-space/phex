from io import StringIO

from phexsec.user import User


class Grant(object):
    def __init__(self, access_token: str, decoded_token: dict):
        self.__access_token = access_token
        self.__decoded_token = decoded_token
        self.__user = User(
            id=decoded_token["sub"],
            login=decoded_token["preferred_username"],
            lastname=decoded_token["family_name"],
            firstname=decoded_token["given_name"],
            email=decoded_token["email"],
        )

    @property
    def access_token(self):
        return self.__access_token

    @property
    def decoded_token(self):
        return self.__decoded_token

    @property
    def user(self):
        return self.__user
