from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, **data) -> Category:
        category = Category(**data)
        self.session.add(category)
        await self.session.flush()
        return category