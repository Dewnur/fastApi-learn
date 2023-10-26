from fastapi import APIRouter, Depends

from app import crud
from app.api.deps import get_current_user, model_id_existing
from app.models import User, Role
from app.schemas.role_schema import IRoleEnum, IRoleRead

router = APIRouter()


@router.get('/{obj_id}')
async def get_role_by_id(
        role_by_id: IRoleRead = Depends(model_id_existing(Role)),
        current_user: User = Depends(get_current_user([IRoleEnum.admin]))
) -> IRoleRead:
    return role_by_id


@router.get('')
async def get_role_list(
        current_user: User = Depends(get_current_user([IRoleEnum.admin]))
) -> list[IRoleRead]:
    role_list = await crud.role.fetch_all()
    return role_list
