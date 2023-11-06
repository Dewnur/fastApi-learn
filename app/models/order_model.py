from datetime import datetime
from typing import TYPE_CHECKING, Sequence
from uuid import UUID

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseUUIDModel
from app.schemas.common_schema import IOrderStatus

if TYPE_CHECKING:
    from app.models.order_item_model import OrderItem
    from app.models.profile_model import Profile


class Order(BaseUUIDModel):
    __tablename__ = "order"

    order_date: Mapped[datetime] = mapped_column(default=datetime.utcnow(), nullable=True)
    status: Mapped[IOrderStatus] = mapped_column(default=None)
    total_amount: Mapped[float] = mapped_column()
    profile_id: Mapped[UUID] = mapped_column(ForeignKey('profile.id'))

    profile: Mapped['Profile'] = relationship(back_populates='orders')
    order_items: Mapped[list['OrderItem']] = relationship(
        back_populates='order', cascade='all, delete', lazy='selectin'
    )
