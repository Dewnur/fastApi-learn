from uuid import UUID

from pydantic import BaseModel, EmailStr


class IUserBase(BaseModel):
    username: str = None
    email: EmailStr = None

    class ConfigDict:
        from_attributes = True


class IUserCreate(IUserBase):
    password: str


class IUserAccess(IUserCreate):
    is_superuser: bool = False
    role_id: UUID = None


class IUserRead(IUserBase):
    id: UUID


class IUserUpdate(IUserBase):
    pass

class LoginData(BaseModel):
    email: EmailStr
    password: str