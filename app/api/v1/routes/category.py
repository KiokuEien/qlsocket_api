from fastapi import APIRouter, status

from app.core.dependencies import CategoryDep
from app.schemas.category import (
    CategoryCreate, CategoryUpdate, CategoryUpdatePartial, CategoryRead, CategoryReadWithProducts
)
from app.api.v1.responses.category import CategoriesResponse, CategoryResponse

router = APIRouter()

# Функция, чтобы определить schema и получить нужный response
def get_response(data, *, uselist: bool = False, with_products_articles: bool = False):
    schema = CategoryRead
    if with_products_articles:
        schema = CategoryReadWithProducts

    if uselist:
        return CategoriesResponse[schema](categories=data)
    return CategoryResponse[schema](category=data)

@router.get('/categories/', summary='Get all categories')
async def get_categories(category_service: CategoryDep, with_products_articles: bool = False):
    categories = await category_service.get_categories(with_products_articles)
    return get_response(categories, uselist=True, with_products_articles=with_products_articles)

@router.get('/categories/{category_id}', summary='Get category by id')
async def get_category(category_service: CategoryDep, category_id: int, with_products_articles: bool = False):
    category = await category_service.get_category(category_id, with_products_articles)
    return get_response(category, with_products_articles=with_products_articles)

@router.post(
    '/categories/', status_code=status.HTTP_201_CREATED, summary='Create category'
)
async def create_category(category_service: CategoryDep, category: CategoryCreate):
    category = await category_service.create_category(category)
    return get_response(category)

@router.put('/categories/{category_id}', summary='Update category by id')
async def update_category(category_service: CategoryDep, category_id: int, category_update: CategoryUpdate):
    category = await category_service.update_category(category_id, category_update)
    return get_response(category)

@router.patch(
    '/categories/{category_id}', summary='Partial update category by id'
)
async def update_category_partial(
        category_service: CategoryDep, category_id: int, category_update_partial: CategoryUpdatePartial
):
    category = await category_service.update_category(category_id, category_update_partial)
    return get_response(category)

@router.delete(
    '/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT, summary='Delete category by id'
)
async def delete_category(category_service: CategoryDep, category_id: int) -> None:
    # delete_category возвращает удаляемый category, но мы используем "чистый" REST подход
    # и вернем 204 без тела ответа
    await category_service.delete_category(category_id)