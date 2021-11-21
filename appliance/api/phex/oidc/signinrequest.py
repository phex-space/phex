import urllib.parse
import uuid

from .metadata import Metadata
from .openidconnectconfiguration import OpenIdConnectConfiguration


class SigninRequest(object):
    def __init__(self, metadata: Metadata, configuration: OpenIdConnectConfiguration):
        self.__metadata = metadata
        self.__configuration = configuration
        self.__state_id = uuid.uuid4().hex
        self.__nonce = uuid.uuid4().hex

    @property
    def state_id(self):
        return self.__state_id

    @property
    def nonce(self):
        return self.__nonce

    async def signin_url(self):
        authorization_endpoint = self.__metadata.authorization_endpoint()
        return "{}?{}".format(
            authorization_endpoint,
            urllib.parse.urlencode(
                {
                    "client_id": self.__configuration.client_id,
                    "redirect_uri": self.__configuration.redirect_uri,
                    "response_type": self.__configuration.response_type,
                    "scope": self.__configuration.scope,
                    "nonce": self.__nonce,
                    "state": self.__state_id,
                }
            ),
        )
