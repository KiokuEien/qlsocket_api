from typing import Sequence

from app.utils.unit_of_work import UnitOfWork
from app.models.brand import Brand
from app.repositories.brand import BrandRepository
from app.core.exceptions import NotFoundError
from app.schemas.brand import BrandCreate, BrandUpdate, BrandUpdatePartial


class BrandService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.repo = BrandRepository(self.uow.session)

    async def create_brand(self, data: BrandCreate) -> Brand:
        brand = await self.repo.create_brand(data)
        return brand

    async def get_brand(
            self,
            brand_id: int,
            with_products: bool = False,
    ) -> Brand:
        brand = await self.repo.get_brand(brand_id=brand_id, with_products=with_products)
        if not brand:
            raise NotFoundError(message='A brand with this id was not found')
        return brand

    async def get_brands(self, with_products: bool = False) -> Sequence[Brand]:
        # REST правило: коллекция существует всегда, даже если пустая
        return await self.repo.get_brands(with_products=with_products)

    async def update_brand(
            self,
            brand_id: int,
            brand_update: BrandUpdate | BrandUpdatePartial,
    ) -> Brand:
        brand = await self.repo.update_brand(
            brand_id=brand_id,
            brand_update=brand_update,
        )
        if not brand:
            raise NotFoundError(message='A brand with this id was not found')
        return brand

    async def delete_brand(self, brand_id: int) -> Brand:
        brand = await self.repo.delete_brand(brand_id=brand_id)
        if not brand:
            raise NotFoundError(message='A brand with this id was not found')
        return brand