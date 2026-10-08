from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attributes import Attribute, ProductAttribute
from app.schemas.attribute import AttributeCreate, AttributeUpdate, AttributeUpdatePartial


class AttributeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_attribute(self, data: AttributeCreate) -> Attribute:
        attribute = Attribute(**data.model_dump())
        self.session.add(attribute)
        await self.session.flush()
        return attribute

    async def get_attribute(
            self,
            attribute_id: int,
            with_products: bool = False,
    ) -> Attribute | None:
        stmt = select(Attribute).where(Attribute.id == attribute_id)
        if with_products:
            stmt = stmt.options(selectinload(Attribute.product_attributes).selectinload(ProductAttribute.product))
        return await self.session.scalar(stmt)

    async def get_attributes(self, with_products: bool = False) -> Sequence[Attribute]:
        stmt = select(Attribute).order_by(Attribute.id)
        if with_products:
            stmt = stmt.options(selectinload(Attribute.product_attributes).selectinload(ProductAttribute.product))
        result = await self.session.scalars(stmt)
        return result.all()

    async def update_attribute(
            self,
            attribute_id: int,
            attribute_update: AttributeUpdate | AttributeUpdatePartial,
    ) -> Attribute | None:
        attribute = await self.session.scalar(select(Attribute).where(Attribute.id == attribute_id))
        if attribute:
            for key, value in attribute_update.model_dump(exclude_unset=True).items():
                setattr(attribute, key, value)
            await self.session.flush()
            await self.session.refresh(attribute)
            return attribute
        return None

    async def delete_attribute(self, attribute_id: int) -> Attribute | None:
        attribute = await self.session.scalar(select(Attribute).where(Attribute.id == attribute_id))
        if not attribute:
            return None
        await self.session.delete(attribute)
        await self.session.flush()
        return attribute