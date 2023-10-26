from app import crud
from app.models import User
from app.schemas.user_schema import IUserCreate
from app.utils.exceptions.common_exception import NameExistException


async def user_existing(user: IUserCreate):
    existing_email = await crud.user.fetch_one(email=user.email)
    if existing_email:
        raise NameExistException(model=User, name=user.email)
    existing_username = await crud.user.fetch_one(username=user.username)
    if existing_username:
        raise NameExistException(model=User, name=user.username)
    return user
