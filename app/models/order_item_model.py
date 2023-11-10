from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseUUIDModel

if TYPE_CHECKING:
    from app.models.order_model import Order
    from app.models.product_model import Product


class OrderItem(BaseUUIDModel):
    __tablename__ = "order_item"

    order_id: Mapped[UUID] = mapped_column(ForeignKey('order.id', ondelete='CASCADE'))
    product_id: Mapped[UUID] = mapped_column(ForeignKey('product.id'))
    quantity: Mapped[int] = mapped_column()
    unit_price: Mapped[float] = mapped_column(Numeric(15, 2))

    order: Mapped['Order'] = relationship(back_populates='order_items')
    product: Mapped['Product'] = relationship(back_populates='order_items', lazy='selectin')
