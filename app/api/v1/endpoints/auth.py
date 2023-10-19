from fastapi import APIRouter, HTTPException

from app import crud
from app.core.security import get_password_hash
from app.db.session import async_session
from app.schemas.user_schema import IUserCreate

router = APIRouter()


@router.post('/register')
async def register_user(user: IUserCreate):
    existing_user = await crud.user.fetch_one(db_session=async_session, email=user.email)
    if existing_user:
        raise HTTPException(status_code=500)
    await crud.user.create(db_session=async_session, obj=user)
