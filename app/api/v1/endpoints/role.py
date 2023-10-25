from fastapi import APIRouter, status, Depends
from fastapi_async_sqlalchemy import db
from fastapi_pagination import Params

from app import crud
from app.api.deps import get_current_user
from app.db.session import async_session
from app.models import User
from app.schemas.role_schema import IRoleEnum, IRoleRead
from app.schemas.user_schema import IUserCreate

router = APIRouter()


@router.get('/{role_id}')
async def create_products(
        current_user: User = Depends(get_current_user([IRoleEnum.admin]))
) -> IRoleRead:
    # role = await crud.role.fetch_one()
    pass