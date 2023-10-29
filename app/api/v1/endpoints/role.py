from fastapi import APIRouter, Depends

from app import crud
from app.api.deps import get_current_user, model_id_existing
from app.models import Role
from app.schemas.role_schema import IRoleEnum, IRoleRead

router = APIRouter()


@router.get(
    '/{obj_id}',
    dependencies=[Depends(get_current_user([IRoleEnum.admin]))]
)
async def get_role_by_id(
        role_by_id: IRoleRead = Depends(model_id_existing(Role)),
) -> IRoleRead:
    return role_by_id


@router.get(
    '',
    dependencies=[Depends(get_current_user([IRoleEnum.admin]))]
)
async def get_role_list(
) -> list[IRoleRead]:
    role_list = await crud.role.fetch_all()
    return role_list
