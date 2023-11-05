from uuid import UUID

from pydantic import BaseModel

from app.schemas.category_schema import ICategoryRead
from app.schemas.image_schema import IImageRead


class IProductBase(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock_quantity: int | None = None
    category_id: UUID | None = None

    class Config:
        from_attributes = True


class IProductCreate(IProductBase):
    pass


class IProductUpdate(IProductBase):
    pass


class IProductRead(IProductBase):
    id: UUID
    category: ICategoryRead | None = None
    image: IImageRead | None = None
