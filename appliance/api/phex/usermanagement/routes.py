import fastapi

router = fastapi.APIRouter(prefix="/user")


@router.get("")
def list_user():
    return {"hallo": "welt!"}
