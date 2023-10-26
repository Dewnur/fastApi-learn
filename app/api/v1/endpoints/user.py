from fastapi import APIRouter, Depends, status, HTTPException

from app import crud
from app.api.deps import get_current_user, model_id_existing
from app.dependencies.user_deps import user_id_existing
from app.models import User
from app.schemas.role_schema import IRoleEnum
from app.schemas.user_schema import IUserRead, IUserUpdate

router = APIRouter()


@router.get('')
async def get_user(
        current_user: IUserRead = Depends(get_current_user())
) -> IUserRead:
    return current_user


@router.get('/{obj_id}')
async def get_user_by_id(
        user_by_id: IUserRead = Depends(model_id_existing(User)),
        current_user: User = Depends(get_current_user([IRoleEnum.admin]))
) -> IUserRead:
    return user_by_id


@router.put('/{user_id}')
async def update_user(
        user: IUserUpdate,
        user_by_id: IUserRead = Depends(user_id_existing),
        current_user: User = Depends(get_current_user())
) -> IUserRead:
    if not current_user.id == user_by_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return await crud.user.update(obj_current=user_by_id, obj_new=user)


@router.delete('/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(
        user_by_id: IUserRead = Depends(user_id_existing),
        current_user: User = Depends(get_current_user([IRoleEnum.admin]))
):
    if user_by_id.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Users cannot delete themselves')
    await crud.user.delete(id=user_by_id.id)
