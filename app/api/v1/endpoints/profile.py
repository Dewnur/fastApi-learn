from fastapi import APIRouter, Depends

from app import crud
from app.api.deps import get_current_user
from app.schemas.profile_schema import IProfileRead, IProfileUpdate
from app.schemas.user_schema import IUserRead

router = APIRouter()


@router.get('')
async def get_profile(
        current_user: IUserRead = Depends(get_current_user())
) -> IProfileRead:
    profile = await crud.profile.fetch_one(user_id=current_user.id)
    return profile


@router.put('')
async def update_profile(
        profile: IProfileUpdate,
        current_user: IUserRead = Depends(get_current_user())
):
    current_profile = await crud.profile.fetch_one(user_id=current_user.id)
    await crud.profile.update(obj_current=current_profile, obj_new=profile)
