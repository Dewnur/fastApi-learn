from uuid import UUID

from pydantic import BaseModel


class ICategoryBase(BaseModel):
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class ICategoryCreate(ICategoryBase):
    pass


class ICategoryUpdate(ICategoryBase):
    pass


class ICategoryRead(ICategoryBase):
    id: UUID
