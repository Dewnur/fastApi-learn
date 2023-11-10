from uuid import UUID

from app.api.deps import get_model_by_id
from app.models import Order


async def order_id_existing(order_id: UUID):
    return await get_model_by_id(obj_id=order_id, model=Order)