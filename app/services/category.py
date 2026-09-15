from typing import Sequence
from sqlalchemy.exc import IntegrityError

from app.utils.unit_of_work import UnitOfWork
from app.models.category import Category
from app.repositories.category import CategoryRepository
from app.core.exceptions import DuplicateError, NotFoundError
from app.schemas.category import CategoryCreate


class CategoryService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.repo = CategoryRepository(self.uow.session)

    async def create_category(self, data: CategoryCreate) -> Category:
        try:
            category = await self.repo.create_category(data)
        except IntegrityError:
            raise DuplicateError(message='Category with this name already exists')
        return category

    async def get_category(
            self,
            category_id: int,
            with_products: bool = False,
    ) -> Category:
        category = await self.repo.get_category(category_id=category_id, with_products=with_products)
        if not category:
            raise NotFoundError(message='Category is not found')
        return category

    async def get_categories(self, with_products: bool = False) -> Sequence[Category]:
        # REST правило: коллекция существует всегда, даже если пустая
        return await self.repo.get_categories(with_products=with_products)
