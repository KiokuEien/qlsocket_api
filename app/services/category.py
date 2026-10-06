from typing import Sequence

from app.utils.unit_of_work import UnitOfWork
from app.models.category import Category
from app.repositories.category import CategoryRepository
from app.core.exceptions import NotFoundError
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryUpdatePartial


class CategoryService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.repo = CategoryRepository(self.uow.session)

    async def create_category(self, data: CategoryCreate) -> Category:
        category = await self.repo.create_category(data)
        return category

    async def get_category(
            self,
            category_id: int,
            with_products: bool = False,
    ) -> Category:
        category = await self.repo.get_category(category_id=category_id, with_products=with_products)
        if not category:
            raise NotFoundError(message='A category with this id was not found')
        return category

    async def get_categories(self, with_products: bool = False) -> Sequence[Category]:
        # REST правило: коллекция существует всегда, даже если пустая
        return await self.repo.get_categories(with_products=with_products)

    async def update_category(
            self,
            category_id: int,
            category_update: CategoryUpdate | CategoryUpdatePartial,
    ) -> Category:
        category = await self.repo.update_category(
            category_id=category_id,
            category_update=category_update,
        )
        if not category:
            raise NotFoundError(message='A category with this id was not found')
        return category

    async def delete_category(self, category_id: int) -> Category:
        category = await self.repo.delete_category(category_id=category_id)
        if not category:
            raise NotFoundError(message='A category with this id was not found')
        return category