class Metadata(object):
    def __init__(self, data: dict):
        self.__data = data

    def authorization_endpoint(self):
        return self.__data["authorization_endpoint"]

    def issuer(self):
        return self.__data["issuer"]

    def userinfo_endpoint(self):
        return self.__data["userinfo_endpoint"]

    def token_endpoint(self):
        return self.__data["token_endpoint"]

    def revocation_endpoint(self):
        return self.__data["revocation_endpoint"]

    def jwks_uri(self):
        return self.__data["jwks_uri"]

    def end_session_endpoint(self):
        return self.__data["end_session_endpoint"]
