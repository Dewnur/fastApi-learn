from uuid import UUID

from pydantic import BaseModel

from app.schemas import IGenderEnum


class IProfileBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    gender: IGenderEnum | None = None
    address: str | None = None
    phone_number: str | None = None

    class Config:
        from_attributes = True


class IProfileCreate(IProfileBase):
    user_id: UUID = None
