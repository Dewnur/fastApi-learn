from app import crud
from app.models import User, Role
from app.schemas.user_schema import IUserCreate
from app.utils.exceptions.common_exception import NameExistException, IdNotFoundException


async def user_existing(user: IUserCreate) -> IUserCreate:
    existing_email = await crud.user.fetch_one(email=user.email)
    if existing_email:
        raise NameExistException(model=User, name=user.email)
    existing_username = await crud.user.fetch_one(username=user.username)
    if existing_username:
        raise NameExistException(model=User, name=user.username)
    existing_role = await crud.role.fetch_one(id=user.role_id)
    if not existing_role:
        raise IdNotFoundException(model=Role, id=user.role_id)
    return user
