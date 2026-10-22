from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.models.product import Product
from app.models.attributes import ProductAttribute
from app.schemas.product import ProductCreate, ProductUpdate, ProductUpdatePartial

class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def sync_product_attributes(self, product: Product, new_attributes: dict[int, str]) -> None:
        existing = {
            pa.attribute_id: pa
            for pa in product.product_attributes
        }
        existing_ids = existing.keys()
        new_ids = new_attributes.keys()

        # Удаляем старые атрибуты
        for attr_id in existing_ids - new_ids:
            await self.session.delete(existing[attr_id])

        # Обновляем существующие атрибуты
        for attr_id in existing_ids & new_ids:
            existing[attr_id].value = new_attributes[attr_id]

        # Добавляем новые атрибуты
        for attr_id in new_ids - existing_ids:
            product.product_attributes.append(
                ProductAttribute(
                    attribute_id=attr_id,
                    value=new_attributes[attr_id],
                )
            )

    async def create_product(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump(exclude={'attributes'}))
        attributes = data.attributes or {}
        product.product_attributes = [
            ProductAttribute(
                attribute_id=attr_id,
                value=attr_value,
            )
            for attr_id, attr_value in attributes.items()
        ]
        self.session.add(product)
        await self.session.flush()

        stmt = (
            select(Product)
            .where(Product.id == product.id)
            .options(joinedload(Product.brand), joinedload(Product.category))
            .options(
                selectinload(Product.product_attributes)
                .selectinload(ProductAttribute.attribute)
            )
        )
        result = await self.session.execute(stmt)
        # scalar_one() не допускает None в типе результата
        return result.scalar_one()

    async def get_product(self, product_sku: str, with_attributes: bool = False) -> Product | None:
        stmt = (
            select(Product)
            .where(Product.sku == product_sku).options(joinedload(Product.brand), joinedload(Product.category))
        )
        if with_attributes:
            stmt = stmt.options(selectinload(Product.product_attributes).selectinload(ProductAttribute.attribute))
        return await self.session.scalar(stmt)

    async def get_products(self, with_attributes: bool = False) -> Sequence[Product]:
        stmt = (
            select(Product)
            .order_by(Product.id).options(joinedload(Product.brand), joinedload(Product.category))
        )
        if with_attributes:
            stmt = stmt.options(
                selectinload(Product.product_attributes).selectinload(ProductAttribute.attribute)
            )
        result = await self.session.scalars(stmt)
        return result.all()

    async def update_product(
            self, product_sku: str, product_update: ProductUpdate | ProductUpdatePartial
    ) -> Product | None:
        stmt = (
            select(Product)
            .where(Product.sku == product_sku)
            .options(joinedload(Product.brand), joinedload(Product.category))
            .options(selectinload(Product.product_attributes).selectinload(ProductAttribute.attribute))
        )
        product: Product | None = await self.session.scalar(stmt)
        if product is None:
            return None
        if isinstance(product_update, ProductUpdate) or 'attributes' in product_update.model_fields_set:
            await self.sync_product_attributes(product, product_update.attributes or {})
        for key, value in product_update.model_dump(exclude={'attributes'}, exclude_unset=True).items():
            setattr(product, key, value)
        await self.session.flush()
        await self.session.refresh(product)
        return product

    async def delete_product(self, product_sku: str):
        product = await self.session.scalar(select(Product).where(Product.sku == product_sku))
        if not product:
            return None
        await self.session.delete(product)
        await self.session.flush()
        return product
