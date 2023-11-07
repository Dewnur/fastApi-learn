from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class IRoleBase(BaseModel):
    name: str

    class ConfigDict:
        from_attributes = True


class IRoleCreate(IRoleBase):
    pass


class IRoleUpdate(IRoleBase):
    pass


class IRoleRead(IRoleBase):
    id: UUID


class IRoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"
