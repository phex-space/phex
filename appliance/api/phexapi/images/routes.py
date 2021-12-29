import datetime
import fastapi
import logging
import os
import sqlalchemy.orm
import shutil

import exif
from fastapi.exceptions import HTTPException
from PIL import Image

from phexapi import auth
from phexcore import services
from phexsec.grant import Grant

from . import schema

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
    filename = image.filename
    filepath = os.path.join(userpath, filename)
    thumbnail_path = None
    try:
        with open(filepath, "wb") as fp:
            shutil.copyfileobj(image.file, fp)
        image_data, thumbnail_path, thumbnail_filename = create_tumbnail(
            userpath, filename
        )
        path = filepath[len(config.images_path) + 1 :]
        modified = datetime.datetime.strptime(
            image_data._getexif()[36867], "%Y:%m:%d %H:%M:%S"
        )
        size = os.path.getsize(filepath)
        mimetype = image.content_type

        from .controller import ImagesService

        images: ImagesService = services.get("images")
        result = await images.create(
            session,
            schema.ImageCreate(
                name=filename,
                thumbnail=thumbnail_filename,
                path=path,
                modified=modified,
                size=size,
                mimetype=mimetype,
            ),
        )
        session.commit()
        session.refresh(result)
        return result
    except Exception as exc:
        _logger.error("Failed upload", exc_info=True)
        os.unlink(filepath)
        if thumbnail_path is not None:
            os.unlink(thumbnail_path)
        session.rollback()
        raise HTTPException(500, exc)
    finally:
        await image.close()


@router.get("/{id}", response_class=fastapi.responses.FileResponse)
async def download_image(
    id: str,
    thumb: bool = False,
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ImagesService

    images: ImagesService = services.get("images")
    image: schema.ImageObject = await images.read(session, id)
    config = services.get("config")
    userpath = os.path.join(config.images_path, grant.user.id)
    if thumb:
        filepath = os.path.join(userpath, image.thumbnail)
    else:
        filepath = os.path.join(userpath, image.name)
    return fastapi.responses.FileResponse(
        filepath, filename=image.name, media_type=image.mimetype
    )


@router.put("/{id}", response_model=schema.ImageObject)
async def update_image(
    id: str,
    data: schema.ImageUpdate,
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ImagesService

    images: ImagesService = services.get("images")
    try:
        result = await images.update(session, id, data)
        session.commit()
        session.refresh(result)
        return result
    except Exception as exc:
        _logger.error("Failed updating image", exc_info=True)
        session.rollback()
        raise HTTPException(500, exc)


@router.delete("/{id}")
async def delete_image(
    id: str,
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ImagesService

    images: ImagesService = services.get("images")
    config = services.get("config")
    userpath = os.path.join(config.images_path, grant.user.id)
    try:
        image = await images.read(session, id)

        await images.delete(session, id)
        filepath = os.path.join(userpath, image.name)
        os.unlink(filepath)
        if image.thumbnail is not None:
            filepath = os.path.join(userpath, image.thumbnail)
            os.unlink(filepath)
        session.commit()
    except Exception as exc:
        _logger.error("Failed delete image", exc_info=True)
        session.rollback()
        raise HTTPException(500, exc)


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


@router.get(
    "/{id}/exif",
)
async def get_image_exif(
    id: str,
    grant: Grant = fastapi.Depends(auth.oidc_scheme),
    session: sqlalchemy.orm.Session = fastapi.Depends(_get_session_creator),
):
    from .controller import ImagesService

    images: ImagesService = services.get("images")
    image = await images.read(session, id)
    config = services.get("config")
    userpath = os.path.join(config.images_path, grant.user.id)
    filepath = os.path.join(userpath, image.name)
    with open(filepath, "rb") as fp:
        exif_data = exif.Image(fp)
        return exif_data.get_all()


def create_tumbnail(path, filename):
    image: Image.Image = Image.open(os.path.join(path, filename))
    filename, ext = os.path.splitext(filename)
    thumbnail_filename = "{}_thumb{}".format(filename, ext)
    thumbnail_path = os.path.join(path, thumbnail_filename)
    image.thumbnail(size=(400, 400))
    image.save(thumbnail_path, optimize=True, quality=80)
    return image, thumbnail_path, thumbnail_filename
