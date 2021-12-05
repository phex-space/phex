import logging
from fastapi.exceptions import HTTPException
import sqlalchemy

from phexapi.auth import oidc_scheme
from . import models, schema

_logger = logging.getLogger(__name__)


class PostsService(object):
    async def create(
        self, session: sqlalchemy.orm.Session, data: schema.PostCreate
    ) -> schema.PostObject:
        grant = oidc_scheme.grant
        new_post = models.Post(**data.dict(), owner_id=grant.user.id)
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return schema.PostObject(**new_post._asdict())

    async def read(self, session: sqlalchemy.orm.Session, id: int) -> schema.PostObject:
        return await self._get_post(session, id)

    async def update(
        self, session: sqlalchemy.orm.Session, id: int, data: schema.PostCreate
    ) -> schema.PostObject:
        post = await self._get_post(session, id)
        post.title = data.title
        post.content = data.content
        post.published = data.published
        session.commit()
        session.refresh(post)
        return post

    async def delete(self, session: sqlalchemy.orm.Session, id: int) -> None:
        post = await self._get_post(session, id)
        session.delete(post)
        session.commit()

    async def list(
        self, session: sqlalchemy.orm.Session, skip: int = 0, limit: int = 20
    ) -> list[schema.PostObject]:
        return (
            session.query(models.Post)
            .order_by(models.Post.updated_at)
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def _get_post(self, session: sqlalchemy.orm.Session, id: int) -> models.Post:
        post = session.query(models.Post).get(id)
        if post is None:
            raise HTTPException(404, detail="Post not found")
        return post
