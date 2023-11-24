from typing import TypeVar, Generic
from uuid import UUID

from fastapi import Request, Depends, HTTPException, status, Path
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.exc import NoResultFound

from app import crud
from app.core.config import get_settings
from app.core.security import JWT_ALGORITHM
from app.crud.crud_base import CRUDBase
from app.db.session import async_session
from app.models import User, Base, Profile
from app.utils.exceptions.auth_exception import (
    TokenExpiredException,
    InvalidTokenException,
    MissingTokenException,
    UserNotFoundException,
    InvalidRoleException,
)
from app.utils.exceptions.common_exception import IdNotFoundException

ModelType = TypeVar("ModelType", bound=Base)


async def get_db_session():
    async with async_session() as session:
        yield session


def get_token(request: Request):
    token = request.cookies.get(get_settings().name_access_token)
    return token


def get_current_user(required_roles: list[str] = None):
    async def current_user(
            token: str = Depends(get_token)
    ) -> User:
        if not token:
            raise MissingTokenException()
        try:
            payload = jwt.decode(
                token,
                key=get_settings().encrypt_key,
                algorithms=JWT_ALGORITHM,
            )
        except ExpiredSignatureError:
            raise TokenExpiredException()
        except JWTError:
            raise InvalidTokenException()
        user_id: str = payload.get('sub')
        if not user_id:
            raise InvalidTokenException()
        user = await crud.user.fetch_one(id=UUID(user_id))
        if not user:
            raise UserNotFoundException()

        if required_roles:
            is_valid_role = False
            for role in required_roles:
                if role == user.role.name:
                    is_valid_role = True

            if not is_valid_role:
                raise InvalidRoleException()
        return user

    return current_user


def model_id_existing(model: Generic[ModelType]):
    async def get_model(obj_id: UUID):
        model_crud = CRUDBase(model)
        obj = await model_crud.fetch_one(id=obj_id)
        if not obj:
            raise IdNotFoundException(model=model, id=obj_id)
        return obj

    return get_model


async def get_model_by_id(obj_id: UUID, model: Generic[ModelType]):
    model_crud = CRUDBase(model)
    obj = await model_crud.fetch_one(id=obj_id)
    if not obj:
        raise IdNotFoundException(model=model, id=obj_id)
    return obj
