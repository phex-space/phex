import fastapi
from fastapi import Depends

from phex.authentication import authentication

router = fastapi.APIRouter(prefix="/user")


@router.get("")
async def list_user(auth=Depends(authentication)):
    return {"hallo": auth}
