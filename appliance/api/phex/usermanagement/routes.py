import fastapi

from phex import authentication

router = fastapi.APIRouter(prefix="/user")


@router.get("")
def list_user(token = fastapi.Depends(authentication.authenticate_user)):
    return {"hallo": token}
