import datetime
import logging

import sqlalchemy
from fastapi.exceptions import HTTPException

from phexapi.auth import oidc_scheme
from . import models, schema

_logger = logging.getLogger(__name__)


class ExhibitionService(object):
    async def create(
        self, session: sqlalchemy.orm.Session, data: schema.ExhibitionCreate
    ) -> schema.ExhibitionObject:
        grant = oidc_scheme.grant
        new_image = models.Exhibition(**data.dict(), owner_id=grant.user.id)
        session.add(new_image)
        return new_image

    async def read(
        self, session: sqlalchemy.orm.Session, id: int
    ) -> schema.ExhibitionObject:
        return await self._get_exhibition(session, id)

    async def update(
        self, session: sqlalchemy.orm.Session, id: int, data: schema.ExhibitionCreate
    ) -> schema.ExhibitionObject:
        exhibition = await self._get_exhibition(session, id)
        exhibition.title = data.title
        exhibition.description = data.description
        exhibition.starts_at = data.starts_at
        exhibition.ends_at = data.ends_at
        return exhibition

    async def delete(self, session: sqlalchemy.orm.Session, id: int) -> None:
        image = await self._get_exhibition(session, id)
        session.delete(image)

    async def list(
        self, session: sqlalchemy.orm.Session, skip: int = 0, limit: int = 20
    ) -> list[schema.ExhibitionInfoObject]:
        grant = oidc_scheme.grant
        return (
            session.query(models.Exhibition)
            .filter_by(owner_id=grant.user.id)
            .order_by(models.Exhibition.starts_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    # async def list_current_active(
    #     self, session: sqlalchemy.orm.Session, skip: int = 0, limit: int = 20
    # ) -> list[schema.ExhibitionInfoObject]:
    #     return (
    #         session.query(models.Exhibition)
    #         .filter(
    #             sqlalchemy.and_(
    #                 models.Exhibition.active == True,
    #                 models.Exhibition.ends_at <= datetime.datetime.now(),
    #             )
    #         )
    #         .order_by(models.Exhibition.starts_at.desc())
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )

    async def _get_exhibition(
        self, session: sqlalchemy.orm.Session, id: int
    ) -> models.Exhibition:
        grant = oidc_scheme.grant
        image = (
            session.query(models.Exhibition)
            .filter_by(id=id, owner_id=grant.user.id)
            .first()
        )
        if image is None:
            raise HTTPException(404, detail="Exhibition not found")
        return image
