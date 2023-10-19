from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseUUIDModel
from app.schemas.common_schema import IGenderEnum

if TYPE_CHECKING:
    from app.models.order_model import Order


class User(BaseUUIDModel):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    gender: Mapped[IGenderEnum] = mapped_column(default=IGenderEnum.other, nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)

    orders: Mapped[list['Order']] = relationship(back_populates='users')
