from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas import IOrderStatus
from app.schemas.order_items_schema import IOrderItemCreate


class IOrderBase(BaseModel):
    order_items: list[IOrderItemCreate]
    status: IOrderStatus
    total_amount: float

    class Config:
        from_attributes = True


class IOrderCreate(IOrderBase):
    profile_id: UUID


class IOrderRead(IOrderBase):
    order_date: datetime
