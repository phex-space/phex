import datetime
import uuid
import fastapi
import logging
import os
import sqlalchemy.orm
import shutil
from fastapi.exceptions import HTTPException

import phexsec

from phexapi.auth import oidc_scheme
from phexcore import services
from phexsec.grant import Grant

from . import schema
from phexapi import auth

_logger = logging.getLogger(__name__)
router = fastapi.APIRouter(prefix="/images")


def _get_session_creator() -> sqlalchemy.orm.Session:
    try:
        database = services.get("database")
        session = database.new_session()
        yield session
    finally:
        session.close()


@router.get(
    "", response_model=list[schema.ImageInfoObject], response_model_exclude_none=True
)
async def list_images(
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ImagesService

    images: ImagesService = services.get("images")
    return await images.list(session)


@router.post("", response_model=schema.ImageObject, response_model_exclude_none=True)
async def upload_image(
    image: fastapi.UploadFile = fastapi.File(...),
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    config = services.get("config")
    userpath = os.path.join(config.images_path, grant.user.id)
    os.makedirs(userpath, exist_ok=True)
    filepath = os.path.join(userpath, image.filename)
    try:
        with open(filepath, "wb") as fp:
            shutil.copyfileobj(image.file, fp)
        path = filepath[len(config.images_path) + 1 :]
        modified = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
        size = os.path.getsize(filepath)
        mimetype = image.content_type

        from .controller import ImagesService

        images: ImagesService = services.get("images")
        return await images.create(
            session,
            schema.ImageCreate(
                name=image.filename,
                path=path,
                modified=modified,
                size=size,
                mimetype=mimetype,
            ),
        )
    except Exception as exc:
        _logger.error("Failed upload", exc_info=True)
        os.unlink(filepath)
        session.rollback()
        raise HTTPException(500, "Failed upload")
    finally:
        await image.close()


@router.get("/{id}", response_class=fastapi.responses.FileResponse)
async def download_image(
    id: str,
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ImagesService

    images: ImagesService = services.get("images")
    image: schema.ImageObject = await images.read(session, id)
    config = services.get("config")
    userpath = os.path.join(config.images_path, grant.user.id)
    filepath = os.path.join(userpath, image.name)
    return fastapi.responses.FileResponse(
        filepath, filename=image.name, media_type=image.mimetype
    )


@router.get(
    "/{id}/metadata",
    response_model=schema.ImageObject,
    response_model_exclude_none=True,
)
async def get_image_metadata(
    id: str,
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ImagesService

    images: ImagesService = services.get("images")
    return await images.read(session, id)
