from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseUUIDModel

if TYPE_CHECKING:
    from app.models.role_model import Role
    from app.models.profile_model import Profile


class User(BaseUUIDModel):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role_id: Mapped[UUID] = mapped_column(ForeignKey('role.id'))
    is_superuser: Mapped[bool] = mapped_column(default=False)

    profile: Mapped['Profile'] = relationship(back_populates='user', cascade="all, delete")
    role: Mapped['Role'] = relationship(back_populates='user', lazy='selectin')
