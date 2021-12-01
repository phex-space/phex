class Metadata(object):
    def __init__(self, data: dict):
        self.__data = data

    @property
    def authorization_endpoint(self):
        return self.__data["authorization_endpoint"]

    @property
    def issuer(self):
        return self.__data["issuer"]

    @property
    def userinfo_endpoint(self):
        return self.__data["userinfo_endpoint"]

    @property
    def token_endpoint(self):
        return self.__data["token_endpoint"]

    @property
    def revocation_endpoint(self):
        return self.__data["revocation_endpoint"]

    @property
    def jwks_uri(self):
        return self.__data["jwks_uri"]

    @property
    def end_session_endpoint(self):
        return self.__data["end_session_endpoint"]
