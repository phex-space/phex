import datetime
import logging
import os
import typing

import fastapi
from fastapi.exceptions import HTTPException
import sqlalchemy.orm


from phexapi import auth
from phexcore import services
from phexsec.grant import Grant

from . import schema
from ..images import schema as images_schema

_logger = logging.getLogger(__name__)
router = fastapi.APIRouter(prefix="/exhibitions")


def _get_session_creator() -> sqlalchemy.orm.Session:
    try:
        database = services.get("database")
        session = database.new_session()
        yield session
    finally:
        session.close()


@router.get("/", response_model=list[schema.ExhibitionInfoObject])
async def list_exhibition(
    id: int,
    skip: int = 0,
    limit: int = 10,
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ExhibitionService

    exhibtions: ExhibitionService = services.get("exhibtions")
    try:
        return await exhibtions.list(session, skip, limit)
    except Exception:
        _logger.error("Failed listing exhibition", exc_info=True)
        raise


@router.get("/current-active", response_model=list[schema.ExhibitionInfoObject])
async def list_exhibition(
    id: int,
    skip: int = 0,
    limit: int = 10,
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ExhibitionService

    exhibtions: ExhibitionService = services.get("exhibtions")
    try:
        return await exhibtions.list_current_active(session, skip, limit)
    except Exception:
        _logger.error("Failed listing active exhibitions", exc_info=True)
        raise


@router.post("", response_model=schema.ExhibitionObject)
async def create_exhibition(
    data: schema.ExhibitionCreate,
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ExhibitionService

    exhibtions: ExhibitionService = services.get("exhibtions")
    try:
        result = await exhibtions.create(session, data)
        session.commit()
        session.refresh(result)
        return result
    except Exception:
        _logger.error("Failed creation of exhibition", exc_info=True)
        session.rollback()
        raise


@router.get("/{id}", response_model=schema.ExhibitionObject)
async def read_exhibition(
    id: int,
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ExhibitionService

    exhibtions: ExhibitionService = services.get("exhibtions")
    try:
        return await exhibtions.read(session, id)
    except Exception:
        _logger.error("Failed reading of exhibition", exc_info=True)
        raise


@router.put("/{id}", response_model=schema.ExhibitionObject)
async def update_exhibition(
    id: int,
    data: schema.ExhibitionCreate,
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ExhibitionService

    exhibtions: ExhibitionService = services.get("exhibtions")
    try:
        result = await exhibtions.update(session, id, data)
        session.commit()
        session.refresh(result)
        return result
    except Exception:
        _logger.error("Failed update of exhibition", exc_info=True)
        session.rollback()
        raise


@router.delete("/{id}")
async def delete_exhibition(
    id: int,
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ExhibitionService

    exhibtions: ExhibitionService = services.get("exhibtions")
    try:
        await exhibtions.delete(session, id)
        session.commit()
    except Exception:
        _logger.error("Failed deletion of exhibition", exc_info=True)
        session.rollback()
        raise


@router.get("/{id}/images/{image_id}", response_class=fastapi.responses.FileResponse)
async def download_exhibition_image(
    id: int,
    image_id: str,
    thumb: bool = False,
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ExhibitionService
    from ..images.controller import ImagesService

    exhibtions: ExhibitionService = services.get("exhibtions")
    images: ImagesService = services.get("images")
    try:
        result = await exhibtions.read(session, id)
        now = datetime.datetime.now()
        if find_index(result.images, lambda obj, index, arr: obj.id == image_id) == -1:
            raise HTTPException(404, "Not found")
        if not result.active or result.starts_at >= now or result.ends_at <= now:
            raise HTTPException(404, "Not found")

        image = await images.read(image_id)
        config = services.get("config")
        userpath = os.path.join(config.images_path, image.owner_id)
        if thumb:
            filepath = os.path.join(userpath, image.thumbnail)
        else:
            filepath = os.path.join(userpath, image.name)
        return fastapi.responses.FileResponse(
            filepath, filename=image.name, media_type=image.mimetype
        )
    except Exception:
        _logger.error("Failed download of image from exhibition", exc_info=True)
        session.rollback()
        raise


@router.put("/{id}/images", response_model=schema.ExhibitionObject)
async def add_exhibition_image(
    id: int,
    data: images_schema.ImageInfoObject,
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ExhibitionService
    from ..images.controller import ImagesService

    exhibtions: ExhibitionService = services.get("exhibtions")
    images: ImagesService = services.get("images")
    try:
        result = await exhibtions.read(session, id)
        image = await images.read(data.id)
        result.images.append(image)
        session.commit()
        session.refresh(result)
        return result
    except Exception:
        _logger.error("Failed add image to exhibition", exc_info=True)
        session.rollback()
        raise


def find_index(
    arr: list, predicate: typing.Callable[[typing.Any, int, list[typing.Any]], bool]
) -> int:
    result = -1
    for obj, index in enumerate(arr):
        if predicate(obj, index, arr):
            result = index
            break
    return result
