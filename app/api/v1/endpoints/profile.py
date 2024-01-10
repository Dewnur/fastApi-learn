from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.deps import get_current_user, get_db_session
from app.dependencies.order_deps import order_id_existing
from app.dependencies.profile_deps import validate_user_profile
from app.models import Profile, Order
from app.schemas.order_items_schema import IOrderItemCreate
from app.schemas.order_schema import IOrderWithItems, IOrderRead
from app.schemas.profile_schema import IProfileRead, IProfileUpdate
from app.schemas.user_schema import IUserRead
from app.services.order_service import create_order

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
) -> IProfileRead:
    current_profile = await crud.profile.fetch_one(user_id=current_user.id)
    return await crud.profile.update(obj_current=current_profile, obj_new=profile)


@router.post(
    path='/{profile_id}/orders',
    status_code=status.HTTP_201_CREATED,
)
async def post_order(
        order_items: list[IOrderItemCreate],
        user_profile: Profile = Depends(validate_user_profile()),
        db_session: AsyncSession = Depends(get_db_session)
) -> IOrderRead:
    return await create_order(
        profile_id=user_profile.id,
        order_items=order_items,
        db_session=db_session
    )


@router.get(
    path='/{profile_id}/orders/{order_id}/itemsList',
    status_code=status.HTTP_200_OK,
)
async def get_profile_order_items(
        user_profile: Profile = Depends(validate_user_profile()),
        order_by_id: Order = Depends(order_id_existing),
) -> IOrderWithItems:
    return await crud.order.fetch_one(id=order_by_id.id)


@router.get(
    path='/{profile_id}/orders/{order_id}',
    status_code=status.HTTP_200_OK,
)
async def get_profile_order(
        order_by_id: Order = Depends(order_id_existing),
        user_profile: Profile = Depends(validate_user_profile()),
) -> IOrderWithItems:
    return await crud.order.fetch_one(id=order_by_id.id)
