from fastapi import APIRouter, status

from app.core.dependencies import ProductDep
from app.schemas.product import (
    ProductRead, ProductUpdate, ProductUpdatePartial, ProductCreate, ProductReadWithAttributes
)
from app.api.v1.responses.product import ProductResponse, ProductsResponse

router = APIRouter()

def get_response(data, *, uselist: bool = False, with_attributes: bool = False):
    schema = ProductRead
    if with_attributes:
        schema = ProductReadWithAttributes
    if uselist:
        return ProductsResponse[schema](products=data)
    return ProductResponse[schema](product=data)

@router.get('/products/', summary='Get all products')
async def get_products(product_service: ProductDep, with_attributes: bool = False):
    products = await product_service.get_products(with_attributes)
    return get_response(products, uselist=True, with_attributes=with_attributes)

@router.get('/products/{product_id}', summary='Get product by article')
async def get_product(product_service: ProductDep, product_id: int, with_attributes: bool = False):
    product = await product_service.get_product(product_id, with_attributes)
    return get_response(product, with_attributes=with_attributes)

@router.post('/products/', summary='Create product', status_code=status.HTTP_201_CREATED)
async def create_product(product_service: ProductDep, product_data: ProductCreate):
    product = await product_service.create_product(product_data)
    return get_response(product, with_attributes=True)

@router.put('/products/{product_id}', summary='Update product by id')
async def update_product(product_service: ProductDep, product_id: int, product_update: ProductUpdate):
    product = await product_service.update_product(product_id, product_update)
    return get_response(product, with_attributes=True)

@router.patch('/products/{product_id}', summary='Partial update product by id')
async def update_product_partial(
        product_service: ProductDep, product_id: int, product_update_partial: ProductUpdatePartial
):
    product = await product_service.update_product(product_id, product_update_partial)
    return get_response(product, with_attributes=True)

@router.delete('/products/{product_id}', summary='Delete product by id', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_service: ProductDep, product_id: int):
    await product_service.delete_product(product_id)

# Добавить brand.name, category.name
# Добавить возможность получать по sku