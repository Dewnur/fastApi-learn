from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseUUIDModel

if TYPE_CHECKING:
    from app.models.product_model import Product


class Discount(BaseUUIDModel):
    __tablename__ = "discount"

    product_id: Mapped[UUID] = mapped_column(ForeignKey('product.id'))
    discount_percentage: Mapped[int] = mapped_column(nullable=False)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False)

    product: Mapped['Product'] = relationship(back_populates='discount')
