from uuid import UUID

from pydantic import BaseModel


class IOrderItemBase(BaseModel):
    product_id: UUID
    quantity: int

    class Config:
        from_attributes = True


class IOrderItemCreate(IOrderItemBase):
    pass


class IOrderItemRead(IOrderItemBase):
    id: UUID
    unit_price: float
