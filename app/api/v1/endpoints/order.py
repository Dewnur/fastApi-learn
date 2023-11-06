from fastapi import APIRouter, status, Depends, HTTPException

from app import crud
from app.api.deps import get_current_user
from app.models import User, Profile
from app.schemas import IOrderStatus
from app.schemas.order_items_schema import IOrderItemCreate
from app.schemas.order_schema import IOrderRead, IOrderCreate
from app.schemas.role_schema import IRoleEnum

router = APIRouter()


@router.post(
    path='',
    status_code=status.HTTP_201_CREATED
)
async def post_order(
        order_items: list[IOrderItemCreate],
        current_user: User = Depends(get_current_user([IRoleEnum.user, IRoleEnum.admin]))
) -> IOrderRead:
    profile: Profile = current_user.profile
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
    order: IOrderCreate = IOrderCreate(
        profile_id=profile.id,
        order_items=order_items,
        status=IOrderStatus.processing,
        total_amount=0,
    )
    return await crud.order.create(order=order)
