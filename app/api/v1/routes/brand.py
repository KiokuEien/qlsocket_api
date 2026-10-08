from fastapi import APIRouter, status

from app.core.dependencies import BrandDep
from app.schemas.brand import BrandCreate, BrandUpdate, BrandUpdatePartial
from app.api.v1.responses.brand import BrandsResponse, BrandResponse

router = APIRouter()

@router.get('/brands/', response_model=BrandsResponse, summary='Get all brands')
async def get_brands(brand_service: BrandDep):
    brands = await brand_service.get_brands()
    return {
        'total': len(brands),
        'brands': brands,
    }

@router.get('/brands/{brand_id}', response_model=BrandResponse)
async def get_brand(brand_service: BrandDep, brand_id: int):
    brand = await brand_service.get_brand(brand_id)
    return {
        'brand': brand,
    }

@router.post('/brands/', response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
async def create_brand(brand_service: BrandDep, brand: BrandCreate):
    brand = await brand_service.create_brand(brand)
    return {
        'brand': brand,
    }

@router.put('/brands/{brand_id}', response_model=BrandResponse)
async def update_brand(brand_service: BrandDep, brand_id: int, brand_update: BrandUpdate):
    brand = await brand_service.update_brand(brand_id, brand_update)
    return {
        'brand': brand,
    }

@router.patch('/brands/{brand_id}', response_model=BrandResponse)
async def update_brand_partial(
        brand_service: BrandDep, brand_id: int, brand_update_partial: BrandUpdatePartial
):
    brand = await brand_service.update_brand(brand_id, brand_update_partial)
    return {
        'brand': brand,
    }

@router.delete(
    '/brands/{brand_id}', status_code=status.HTTP_204_NO_CONTENT
)
async def delete_brand(brand_service: BrandDep, brand_id: int) -> None:
    await brand_service.delete_brand(brand_id)