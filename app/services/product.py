from typing import Sequence
from enum import StrEnum

from app.utils.unit_of_work import UnitOfWork
from app.models.product import Product
from app.repositories.product import ProductRepository
from app.core.exceptions import NotFoundError
from app.schemas.product import ProductCreate, ProductUpdate, ProductUpdatePartial

class ErrorsTexts(StrEnum):
    NOT_FOUND_BY_ID = 'A product with this SKU was not found'

class ProductService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.repo = ProductRepository(self.uow.session)

    async def create_product(self, data: ProductCreate) -> Product:
        product = await self.repo.create_product(data)
        return product

    async def get_product(
            self,
            product_sku: str,
            with_attributes: bool = False,
    ) -> Product:
        product = await self.repo.get_product(product_sku=product_sku, with_attributes=with_attributes)
        if not product:
            raise NotFoundError(message=ErrorsTexts.NOT_FOUND_BY_ID)
        return product

    async def get_products(self, with_attributes: bool = False) -> Sequence[Product]:
        return await self.repo.get_products(with_attributes=with_attributes)

    async def update_product(
            self,
            product_sku: str,
            product_update: ProductUpdate | ProductUpdatePartial,
    ) -> Product:
        product = await self.repo.update_product(
            product_sku=product_sku,
            product_update=product_update,
        )
        if not product:
            raise NotFoundError(message=ErrorsTexts.NOT_FOUND_BY_ID)
        return product

    async def delete_product(self, product_sku: str) -> Product:
        product = await self.repo.delete_product(product_sku=product_sku)
        if not product:
            raise NotFoundError(message=ErrorsTexts.NOT_FOUND_BY_ID)
        return product