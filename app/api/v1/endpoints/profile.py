from fastapi import APIRouter, Depends, status, HTTPException

from app import crud
from app.api.deps import get_current_user, model_id_existing
from app.models import User, Profile
from app.schemas import IOrderStatus
from app.schemas.order_items_schema import IOrderItemCreate
from app.schemas.order_schema import IOrderRead, IOrderCreate
from app.schemas.profile_schema import IProfileRead, IProfileUpdate
from app.schemas.role_schema import IRoleEnum
from app.schemas.user_schema import IUserRead

router = APIRouter()


@router.get(
    path='',
    status_code=status.HTTP_200_OK
)
async def get_profile(
        current_user: IUserRead = Depends(get_current_user())
) -> IProfileRead:
    profile = await crud.profile.fetch_one(user_id=current_user.id)
    return profile


@router.put(
    path='',
    status_code=status.HTTP_201_CREATED
)
async def update_profile(
        profile: IProfileUpdate,
        current_user: IUserRead = Depends(get_current_user())
):
    current_profile = await crud.profile.fetch_one(user_id=current_user.id)
    await crud.profile.update(obj_current=current_profile, obj_new=profile)


@router.post(
    path='/{obj_id}/orders',
    status_code=status.HTTP_201_CREATED
)
async def post_order(
        order_items: list[IOrderItemCreate],
        current_user: User = Depends(get_current_user([IRoleEnum.user])),
        profile_by_id: Profile = Depends(model_id_existing(Profile))
) -> IOrderRead:
    if not order_items:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Order items list is empty'
        )

    profile: Profile = current_user.profile
    if not profile.id == profile_by_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )
    if not profile.phone_number:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='No phone number provided'
        )
    if not profile.address:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Address not specified'
        )
    return await crud.order.create(
        order=IOrderCreate(
            profile_id=profile.id,
            order_items=order_items,
            status=IOrderStatus.processing,
            total_amount=0,
        )
    )
