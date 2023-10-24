from fastapi import HTTPException
from starlette import status

from app import crud
from app.db.session import async_session
from app.schemas.user_schema import IUserCreate


async def user_existing(user: IUserCreate) -> IUserCreate:
    existing_email = await crud.user.fetch_one(db_session=async_session, email=user.email)
    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    existing_username = await crud.user.fetch_one(db_session=async_session, username=user.username)
    if existing_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    existing_role = await crud.role.fetch_one(db_session=async_session, id=user.role_id)
    if not existing_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
