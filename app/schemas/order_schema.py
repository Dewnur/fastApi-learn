from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas import IOrderStatus
from app.schemas.order_items_schema import IOrderItemCreate, IOrderItemRead


class IOrderBase(BaseModel):
    status: IOrderStatus = IOrderStatus.processing
    total_amount: float = 0.0

    class ConfigDict:
        from_attributes = True


class IOrderCreate(IOrderBase):
    profile_id: UUID
    order_items: list[IOrderItemCreate]


class IOrderRead(IOrderBase):
    id: UUID
    order_date: datetime


class IOrderWithItems(IOrderRead):
    order_items: list[IOrderItemRead]
