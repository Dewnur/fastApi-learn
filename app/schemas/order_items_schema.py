from uuid import UUID

from pydantic import BaseModel

from app.schemas.product_schema import IProductRead


class IOrderItemBase(BaseModel):
    product_id: UUID
    quantity: int

    class ConfigDict:
        from_attributes = True


class IOrderItemCreate(IOrderItemBase):
    pass


class IOrderItemRead(IOrderItemBase):
    id: UUID
    unit_price: float
    product: IProductRead
