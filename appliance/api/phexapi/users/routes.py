import typing
import fastapi
import sqlalchemy

import phexsec
from phexapi.auth import oidc_scheme
from phexcore import services
from phexsec.grant import Grant

from . import schema

router = fastapi.APIRouter(prefix="/users")


def _get_session_creator() -> sqlalchemy.orm.Session:
    try:
        database = services.get("database")
        session = database.new_session()
        yield session
    finally:
        session.close()


@router.get("/me", response_model=schema.UserObject)
async def read_post(
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
    grant: phexsec.Grant = fastapi.Depends(oidc_scheme),
) -> list[schema.UserObject]:
    from . import controller

    users: controller.UserService = services.get("users")
    return await users.read(session, grant.user.id)
