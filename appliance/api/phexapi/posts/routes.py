import fastapi
from phexsec.grant import Grant
import sqlalchemy

import phexsec
from phexapi.auth import oidc_scheme
from phexcore import services

from . import schema

router = fastapi.APIRouter(prefix="/posts")


def _get_session_creator() -> sqlalchemy.orm.Session:
    try:
        database = services.get("database")
        session = database.new_session()
        yield session
    finally:
        session.close()


@router.get("")
async def list_posts(
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
    grant: phexsec.Grant = fastapi.Depends(oidc_scheme),
    consent: phexsec.Consent = fastapi.Depends(
        oidc_scheme.approve("api", phexsec.Access("list", "Post"))
    ),
) -> list[schema.PostObject]:
    from .controller import PostsService

    controller: PostsService = services.get("posts")
    return await controller.list(session)


@router.post("", status_code=201)
async def create_post(
    post: schema.PostCreate,
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
    consent: phexsec.Consent = fastapi.Depends(
        oidc_scheme.approve("api", phexsec.Access("write", "Post"))
    ),
) -> schema.PostObject:
    from .controller import PostsService

    controller: PostsService = services.get("posts")
    return await controller.create(session, post)


@router.get("/{id}")
async def read_post(
    id: int,
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
    consent: phexsec.Consent = fastapi.Depends(
        oidc_scheme.approve("api", phexsec.Access("read", "Post"))
    ),
) -> list[schema.PostObject]:
    from .controller import PostsService

    controller: PostsService = services.get("posts")
    return await controller.read(session, id)


@router.put("/{id}")
async def update_post(
    id: int,
    post: schema.PostCreate,
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
    consent: phexsec.Consent = fastapi.Depends(
        oidc_scheme.approve("api", phexsec.Access("write", "Post"))
    ),
) -> list[schema.PostObject]:
    from .controller import PostsService

    controller: PostsService = services.get("posts")
    return await controller.update(session, id, post)


@router.delete("/{id}", status_code=204)
async def delete_post(
    id: int,
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
    consent: phexsec.Consent = fastapi.Depends(
        oidc_scheme.approve("api", phexsec.Access("write", "Post"))
    ),
) -> list[schema.PostObject]:
    from .controller import PostsService

    controller: PostsService = services.get("posts")
    return await controller.delete(session, id)
