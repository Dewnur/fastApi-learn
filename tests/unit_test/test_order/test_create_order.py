from uuid import UUID

import pytest

from app import crud
from app.schemas.order_schema import IOrderCreate
from app.services.order_service import create_order
from app.utils.exceptions.common_exception import IdNotFoundException
from app.utils.exceptions.order_items_excemption import EmptyOrderItemsException
from app.utils.exceptions.product_exceptions import InsufficientStockException


@pytest.fixture
def valid_order_create() -> IOrderCreate:
    return IOrderCreate(
        order_items=[
            {
                "product_id": "00000000-0000-0000-0000-000000000001",
                "quantity": 1
            }
        ],
        profile_id="00000000-0000-0000-0000-000000000001",
    )


async def test_service_create_order_success(valid_order_create, get_db_session):
    order = await create_order(
        profile_id=valid_order_create.profile_id,
        order_items=valid_order_create.order_items,
        db_session=get_db_session
    )
    assert order


async def test_create_order_empty_items(get_db_session):
    with pytest.raises(EmptyOrderItemsException):
        await create_order(
            profile_id=UUID("00000000-0000-0000-0000-000000000001"),
            order_items=[],
            db_session=get_db_session
        )


async def test_create_order_invalid_product_id(valid_order_create, get_db_session):
    valid_order_create.order_items[0].product_id = UUID("13000000-0000-0000-0000-000000000001")
    with pytest.raises(IdNotFoundException):
        await create_order(
            profile_id=valid_order_create.profile_id,
            order_items=valid_order_create.order_items,
            db_session=get_db_session
        )


async def test_create_order_insufficient_stock(valid_order_create, get_db_session):
    valid_order_create.order_items[0].quantity = 10000000
    with pytest.raises(InsufficientStockException):
        await create_order(
            profile_id=valid_order_create.profile_id,
            order_items=valid_order_create.order_items,
            db_session=get_db_session
        )


async def test_create_order_total_calculation(valid_order_create, get_db_session):
    order = await create_order(
        profile_id=valid_order_create.profile_id,
        order_items=valid_order_create.order_items,
        db_session=get_db_session
    )

    async def get_product_price(product_id: UUID) -> float:
        product = await crud.product.fetch_one(id=product_id, db_session=get_db_session)
        return product.price

    expected_total = 0
    for item in valid_order_create.order_items:
        expected_total += item.quantity * await get_product_price(item.product_id)

    assert order.total_amount == expected_total
