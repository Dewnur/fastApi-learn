from uuid import UUID

from pydantic import BaseModel


class IProductCreate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock_quantity: int | None = None
    category_id: UUID | None = None
