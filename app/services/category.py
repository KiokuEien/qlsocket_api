from sqlalchemy.exc import IntegrityError

from app.utils.unit_of_work import UnitOfWork
from app.models.category import Category
from app.repositories.category import CategoryRepository
from app.core.exceptions import DuplicateError


class CategoryService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_category(
            self,
            name: str,
            description: str | None = None,
    ) -> Category:
        repo = CategoryRepository(self.uow.session)
        try:
            category = await repo.create_category(name=name, description=description)
        except IntegrityError:
            raise DuplicateError(message='Category with this name already exists')
        return category
