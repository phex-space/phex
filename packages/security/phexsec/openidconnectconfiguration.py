class OpenIdConnectConfiguration(object):
    def __init__(
        self,
        issuer: str,
        client_id: str,
        secret: str,
        redirect_uri: str,
        response_type: str,
        scope: str,
    ):
        self.__issuer = issuer
        self.__client_id = client_id
        self.__secret = secret
        self.__redirect_uri = redirect_uri
        self.__response_type = response_type
        self.__scope = scope

    @property
    def issuer(self):
        return self.__issuer

    @property
    def client_id(self):
        return self.__client_id

    @property
    def secret(self):
        return self.__secret

    @property
    def redirect_uri(self):
        return self.__redirect_uri

    @property
    def response_type(self):
        return self.__response_type

    @property
    def scope(self):
        return self.__scope
