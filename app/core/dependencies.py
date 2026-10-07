from fastapi import Depends
from typing import Annotated, AsyncGenerator

from app.utils.unit_of_work import UnitOfWork
from app.services.category import CategoryService
from app.services.brand import BrandService

async def get_uow() -> AsyncGenerator[UnitOfWork]:
    async with UnitOfWork() as uow:
        yield uow

UowDep = Annotated[UnitOfWork, Depends(get_uow)]

async def get_category_service(uow: UowDep) -> CategoryService:
    return CategoryService(uow)

async def get_brand_service(uow: UowDep) -> BrandService:
    return BrandService(uow)

CategoryDep = Annotated[CategoryService, Depends(get_category_service)]
BrandDep = Annotated[BrandService, Depends(get_brand_service)]