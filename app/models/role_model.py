from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseUUIDModel

if TYPE_CHECKING:
    from app.models.user_model import User


class Role(BaseUUIDModel):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(nullable=False)

    user: Mapped[list['User']] = relationship(back_populates='role')
