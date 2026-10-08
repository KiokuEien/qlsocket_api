from fastapi import Depends
from typing import Annotated, AsyncGenerator

from app.utils.unit_of_work import UnitOfWork
from app.services.category import CategoryService
from app.services.brand import BrandService
from app.services.attribute import AttributeService

async def get_uow() -> AsyncGenerator[UnitOfWork]:
    async with UnitOfWork() as uow:
        yield uow

UowDep = Annotated[UnitOfWork, Depends(get_uow)]

async def get_category_service(uow: UowDep) -> CategoryService:
    return CategoryService(uow)

async def get_brand_service(uow: UowDep) -> BrandService:
    return BrandService(uow)

async def get_attribute_service(uow: UowDep) -> AttributeService:
    return AttributeService(uow)


CategoryDep = Annotated[CategoryService, Depends(get_category_service)]
BrandDep = Annotated[BrandService, Depends(get_brand_service)]
AttributeDep = Annotated[AttributeService, Depends(get_attribute_service)]