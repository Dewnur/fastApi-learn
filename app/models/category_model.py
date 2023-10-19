from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseUUIDModel

if TYPE_CHECKING:
    from app.models.product_model import Product


class Category(BaseUUIDModel):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)

    products: Mapped[list['Product']] = relationship(back_populates='categories')
