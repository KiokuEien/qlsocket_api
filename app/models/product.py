from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Numeric, ForeignKey, Index
from decimal import Decimal

from app.models.base import Base
from app.models.mixins import BaseMixin

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.attributes import ProductAttribute

class Product(Base, BaseMixin):
    __table_args__ = (
        Index('idx_product_sku', 'sku'),
    )

    sku: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str| None] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    category: Mapped[Category] = relationship(
        'Category', back_populates='products', lazy='raise', uselist=False
    )
    product_attributes: Mapped[list[ProductAttribute]] = relationship(
        'ProductAttribute', back_populates='product', lazy='raise'
    )