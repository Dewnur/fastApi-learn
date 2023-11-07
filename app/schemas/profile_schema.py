from uuid import UUID

from pydantic import BaseModel

from app.schemas import IGenderEnum
from app.schemas.user_schema import IUserRead
from app.utils.phone_type import PhoneType


class IProfileBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    gender: IGenderEnum | None = None
    address: str | None = None
    phone_number: PhoneType | None = None

    class ConfigDict:
        from_attributes = True


class IProfileCreate(IProfileBase):
    user_id: UUID = None


class IProfileRead(IProfileBase):
    id: UUID
    user: IUserRead


class IProfileUpdate(IProfileBase):
    pass
