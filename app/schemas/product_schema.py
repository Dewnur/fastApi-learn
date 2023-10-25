from uuid import UUID

from pydantic import BaseModel


class IProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: UUID
