from io import StringIO


class Grant(object):
    def __init__(self, access_token: str, decoded_token: dict):
        self.__access_token = access_token
        self.__user = decoded_token

    @property
    def access_token(self):
        return self.__access_token

    @property
    def user(self):
        return self.__user

    def __repr__(self):
        with StringIO() as buffer:
            buffer.write('Grant("')
            buffer.write(self.access_token)
            buffer.write('", ')
            buffer.write(repr(self.user))
            buffer.write(")")
            return buffer.getvalue()
