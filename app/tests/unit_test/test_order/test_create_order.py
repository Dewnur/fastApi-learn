import pytest

from app.schemas.order_schema import IOrderCreate
from app.services.order_service import create_order


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
