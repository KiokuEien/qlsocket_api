from typing import TYPE_CHECKING
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import BaseMixin

if TYPE_CHECKING:
    from app.models.product import Product

class Brand(Base, BaseMixin):
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(Text)

    products: Mapped[list[Product]] = relationship(
        'Product', back_populates='brand', lazy='raise'
    )