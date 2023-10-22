from pydantic import BaseModel, EmailStr


class IUserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class IUserRead(IUserCreate):
    pass
