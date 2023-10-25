from uuid import UUID

from app import crud
from app.models import User
from app.schemas.user_schema import IUserCreate
from app.utils.exceptions.common_exception import NameExistException, IdNotFoundException


async def user_existing(user: IUserCreate):
    existing_email = await crud.user.fetch_one(email=user.email)
    if existing_email:
        raise NameExistException(model=User, name=user.email)
    existing_username = await crud.user.fetch_one(username=user.username)
    if existing_username:
        raise NameExistException(model=User, name=user.username)
    return user


async def user_id_existing(user_id: UUID):
    user = await crud.user.fetch_one(id=user_id)
    if not user:
        raise IdNotFoundException(model=User, id=user_id)
    return user
