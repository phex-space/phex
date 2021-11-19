import fastapi
from fastapi import Depends

from phex.authentication import approve
from phex.oidc import Access, Consent

router = fastapi.APIRouter(prefix="/user")


@router.get("")
async def list_user(
    consent: Consent = Depends(
        approve(Access("read", "package"), Access("write", "package"))
    )
):
    return {"consent": consent}
