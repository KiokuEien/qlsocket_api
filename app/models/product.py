from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, Numeric, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import BaseMixin

if TYPE_CHECKING:
    from app.models.brand import Brand
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
    brand_id: Mapped[int] = mapped_column(
        ForeignKey('brands.id', ondelete='CASCADE', name='fk_product_brand_id')
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='CASCADE', name='fk_product_category_id')
    )

    brand: Mapped[Brand] = relationship(
        'Brand', back_populates='products', lazy='raise', uselist=False
    )
    category: Mapped[Category] = relationship(
        'Category', back_populates='products', lazy='raise', uselist=False
    )
    product_attributes: Mapped[list[ProductAttribute]] = relationship(
        'ProductAttribute', back_populates='product', lazy='raise'
    )