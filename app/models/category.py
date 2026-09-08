from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text

from app.models.base import Base
from app.models.mixins import BaseMixin

if TYPE_CHECKING:
    from app.models.product import Product

class Category(Base, BaseMixin):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text)

    products: Mapped[list[Product]] = relationship('Product', back_populates='category', lazy='raise')