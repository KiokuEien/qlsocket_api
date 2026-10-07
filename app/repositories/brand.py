from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandUpdate, BrandUpdatePartial

class BrandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_brand(self, data: BrandCreate) -> Brand:
        brand = Brand(**data.model_dump())
        self.session.add(brand)
        await self.session.flush()
        return brand

    async def get_brand(
            self,
            brand_id: int,
            with_products: bool = False,
    ) -> Brand | None:
        stmt = select(Brand).where(Brand.id == brand_id)
        if with_products:
            stmt = stmt.options(selectinload(Brand.products))
        return await self.session.scalar(stmt)

    async def get_brands(self, with_products: bool = False) -> Sequence[Brand]:
        stmt = select(Brand).order_by(Brand.id)
        if with_products:
            stmt = stmt.options(selectinload(Brand.products))
        result = await self.session.scalars(stmt)
        return result.all()

    async def update_brand(
            self,
            brand_id: int,
            brand_update: BrandUpdate | BrandUpdatePartial,
    ) -> Brand | None:
        brand = await self.session.scalar(select(Brand).where(Brand.id == brand_id))
        if brand:
            for key, value in brand_update.model_dump(exclude_unset=True).items():
                setattr(brand, key, value)
            await self.session.flush()
            # После flush() некоторые поля (например, updated_at) протухают, поэтому нужно перезагрузить объект из бд
            await self.session.refresh(brand)
            return brand
        return None

    async def delete_brand(self, brand_id: int) -> Brand | None:
        brand = await self.session.scalar(select(Brand).where(Brand.id == brand_id))
        if not brand:
            return None
        await self.session.delete(brand)
        await self.session.flush()
        return brand