import fastapi
from fastapi import Depends
from starlette.requests import Request

from phex.authentication import authentication
from phex.oidc.metadata import Metadata
from phex.oidc.openidconnectconfiguration import OpenIdConnectConfiguration
from phex.oidc.signinrequest import SigninRequest

router = fastapi.APIRouter(prefix="/user")


@router.get("")
async def list_user(auth=Depends(authentication)):
    return {"hallo": auth}
