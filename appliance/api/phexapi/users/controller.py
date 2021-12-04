import logging
import sqlalchemy
from fastapi.exceptions import HTTPException
from async_lru import alru_cache

from phexapi.auth import oidc_scheme
from phexcore import services
from phexsec import User as UserSecurity

from . import models, schema

_logger = logging.getLogger(__name__)


class UserService(object):
    async def create(
        self, session: sqlalchemy.orm.Session, data: schema.UserCreate
    ) -> schema.UserObject:
        new_user = models.User(**data.dict())
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return schema.UserObject(**new_user._asdict())

    async def read(self, session: sqlalchemy.orm.Session, id: str) -> schema.UserObject:
        user = await self._get_user(session, id)
        return schema.UserObject(**user._asdict())

    async def update(
        self, session: sqlalchemy.orm.Session, id: str, data: schema.UserCreate
    ) -> schema.UserObject:
        user = await self._get_user(session, id)
        user.lastname = data.lastname
        user.firstname = data.firstname
        user.email = data.email
        session.commit()
        session.refresh(user)
        return schema.UserObject(**user._asdict())

    async def _get_user(self, session: sqlalchemy.orm.Session, id: str) -> models.User:
        user = session.query(models.User).get(id)
        if user is None:
            raise HTTPException(404, detail="User not found")
        return user

    async def handle_authorized_user(self, new_user: schema.UserCreate):
        with services.get("database").new_session() as session:
            user = session.query(models.User).get(new_user.id)
            if user is None:
                user = await self.create(session, new_user)
                _logger.debug("User created: {}".format(user))
            elif self._should_update(user, new_user):
                user = await self.update(session, new_user.id, new_user)
                _logger.debug("User updated: {}".format(user))

    def _should_update(self, user: models.User, foreign: UserSecurity):
        return (
            user.lastname != foreign.lastname
            or user.firstname != foreign.firstname
            or user.email != foreign.email
        )
