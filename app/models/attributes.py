from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, UniqueConstraint, Index

from app.models.base import Base
from app.models.mixins import BaseMixin

if TYPE_CHECKING:
    from app.models.product import Product

class Attribute(Base, BaseMixin):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text)

    product_attributes: Mapped[list[ProductAttribute]] = relationship(
        'ProductAttribute', back_populates='attribute', lazy='raise'
    )

class ProductAttribute(Base, BaseMixin):
    __tablename__ = 'product_attributes'
    __table_args__ = (
        UniqueConstraint('product_id', 'attribute_id', name='idx_unique_product_attribute'),
        Index('idx_pa_product_id', 'product_id'),
        Index('idx_pa_attribute_id', 'attribute_id'),
        Index('idx_pa_attribute_value', 'attribute_id', 'value'),
        Index('idx_pa_product_attribute', 'product_id', 'attribute_id'),
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE', name='fk_pa_product_id')
    )
    attribute_id: Mapped[int] = mapped_column(
        ForeignKey('attributes.id', ondelete='CASCADE', name='fk_pa_attribute_id')
    )
    value: Mapped[str] = mapped_column(String(255))


    product: Mapped[Product] = relationship(
        'Product', back_populates='product_attributes', lazy='raise', uselist=False
    )
    attribute: Mapped[Attribute] = relationship(
        'Attribute', back_populates='product_attributes', lazy='raise', uselist=False
    )
