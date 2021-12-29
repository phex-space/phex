import logging
from fastapi.exceptions import HTTPException
import sqlalchemy

from phexapi.auth import oidc_scheme
from . import models, schema

_logger = logging.getLogger(__name__)
max_amount_of_images = 25


class ImagesService(object):
    async def create(
        self, session: sqlalchemy.orm.Session, data: schema.ImageCreate
    ) -> schema.ImageObject:
        grant = oidc_scheme.grant
        image_count = (
            session.query(models.Image)
            .filter_by(owner_id=grant.user.id)
            .order_by(models.Image.title)
            .count()
        )
        if image_count >= max_amount_of_images:
            raise HTTPException(
                507,
                detail={
                    "error": "NoMoreStorage",
                    "message": "You already store {} images. You only can delete one.".format(
                        max_amount_of_images
                    ),
                },
            )
        new_image = models.Image(**data.dict(), owner_id=grant.user.id)
        session.add(new_image)
        return new_image

    async def read(
        self, session: sqlalchemy.orm.Session, id: str
    ) -> schema.ImageObject:
        return await self._get_image(session, id)

    async def update(
        self, session: sqlalchemy.orm.Session, id: str, data: schema.ImageUpdate
    ) -> schema.ImageObject:
        image = await self._get_image(session, id)
        image.title = data.title
        image.description = data.description
        return image

    async def delete(self, session: sqlalchemy.orm.Session, id: str) -> None:
        image = await self._get_image(session, id)
        session.delete(image)

    async def list(
        self, session: sqlalchemy.orm.Session, skip: int = 0, limit: int = 20
    ) -> list[schema.ImageInfoObject]:
        grant = oidc_scheme.grant
        return (
            session.query(models.Image)
            .filter_by(owner_id=grant.user.id)
            .order_by(models.Image.title)
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def _get_image(
        self, session: sqlalchemy.orm.Session, id: str
    ) -> models.Image:
        grant = oidc_scheme.grant
        image = (
            session.query(models.Image).filter_by(id=id, owner_id=grant.user.id).first()
        )
        if image is None:
            raise HTTPException(404, detail="Image not found")
        return image
