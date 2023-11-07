from uuid import UUID

from pydantic import BaseModel


class IImageBase(BaseModel):
    path: str
    name: str
    format: str

    class ConfigDict:
        from_attributes = True


class IImageUpdate(IImageBase):
    pass


class IImageRead(IImageBase):
    id: UUID
