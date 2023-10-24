from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models import User
from app.schemas import IGenderEnum


class IUserBase(BaseModel):
    username: str = None
    email: EmailStr = None
    role_id: UUID = None
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None
    gender: IGenderEnum = None
    address: str = None
    phone_number: str = None

    class Config:
        from_attributes = True


class IUserCreate(IUserBase):
    password: str

    class Config:
        from_attributes = True


class IUserRead(IUserBase):
    id: UUID
