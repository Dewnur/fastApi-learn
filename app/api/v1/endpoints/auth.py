from fastapi import APIRouter, HTTPException, status, Response, Depends
from pydantic import EmailStr

from app import crud
from app.core.config import get_settings
from app.core.security import create_access_token
from app.db.session import async_session
from app.dependencies.user_deps import user_existing
from app.schemas.role_schema import IRoleEnum
from app.schemas.user_schema import IUserCreate

router = APIRouter()


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(
        user: IUserCreate = Depends(user_existing)
):
    existing_role = await crud.role.fetch_one(db_session=async_session, id=user.role_id)
    if not existing_role.name == IRoleEnum.user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await crud.user.create(db_session=async_session, obj=user)


@router.post('/login')
async def login_user(
        response: Response,
        email: EmailStr,
        password: str
):
    auth_user = await crud.user.authenticate(db_session=async_session,
                                             obj=IUserCreate(email=email, password=password))
    if not auth_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token(auth_user.id)
    response.set_cookie(get_settings().name_access_token, access_token, httponly=True)
    return {"message": "Authentication successful", "access_token": access_token}


@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout_user(response: Response):
    response.delete_cookie(get_settings().name_access_token)
