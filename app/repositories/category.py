from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import CategoryCreate


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, data: CategoryCreate) -> Category:
        category = Category(**data.model_dump())
        self.session.add(category)
        await self.session.flush()
        return category

    async def get_category(
            self,
            category_id: int,
            with_products: bool = False,
    ) -> Category | None:
        stmt = select(Category).where(Category.id == category_id)
        if with_products:
            stmt = stmt.options(selectinload(Category.products))
        return await self.session.scalar(stmt)

    async def get_categories(self, with_products: bool = False) -> Sequence[Category]:
        stmt = select(Category).order_by(Category.id)
        if with_products:
            stmt = stmt.options(selectinload(Category.products))
        result = await self.session.scalars(stmt)
        return result.all()