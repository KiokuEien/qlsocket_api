from typing import Sequence

from app.utils.unit_of_work import UnitOfWork
from app.models.attributes import Attribute
from app.repositories.attribute import AttributeRepository
from app.core.exceptions import NotFoundError
from app.schemas.attribute import AttributeCreate, AttributeUpdate, AttributeUpdatePartial


class AttributeService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.repo = AttributeRepository(self.uow.session)

    async def create_attribute(self, data: AttributeCreate) -> Attribute:
        attribute = await self.repo.create_attribute(data)
        return attribute

    async def get_attribute(
            self,
            attribute_id: int,
            with_products: bool = False,
    ) -> Attribute:
        attribute = await self.repo.get_attribute(attribute_id=attribute_id, with_products=with_products)
        if not attribute:
            raise NotFoundError(message='An attribute with this id was not found')
        return attribute

    async def get_attributes(self, with_products: bool = False) -> Sequence[Attribute]:
        # REST правило: коллекция существует всегда, даже если пустая
        return await self.repo.get_attributes(with_products=with_products)

    async def update_attribute(
            self,
            attribute_id: int,
            attribute_update: AttributeUpdate | AttributeUpdatePartial,
    ) -> Attribute:
        attribute = await self.repo.update_attribute(
            attribute_id=attribute_id,
            attribute_update=attribute_update,
        )
        if not attribute:
            raise NotFoundError(message='An attribute with this id was not found')
        return attribute

    async def delete_attribute(self, attribute_id: int) -> Attribute:
        attribute = await self.repo.delete_attribute(attribute_id=attribute_id)
        if not attribute:
            raise NotFoundError(message='An attribute with this id was not found')
        return attribute