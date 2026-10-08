from fastapi import APIRouter, status

from app.core.dependencies import CategoryDep
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryUpdatePartial
from app.api.v1.responses.category import CategoriesResponse, CategoryResponse

router = APIRouter()

@router.get('/categories/', response_model=CategoriesResponse, summary='Get all categories')
async def get_categories(category_service: CategoryDep):
    categories = await category_service.get_categories()
    return {
        'total': len(categories),
        'categories': categories,
    }

@router.get('/categories/{category_id}', response_model=CategoryResponse)
async def get_category(category_service: CategoryDep, category_id: int):
    category = await category_service.get_category(category_id)
    return {
        'category': category,
    }

@router.post('/categories/', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category_service: CategoryDep, category: CategoryCreate):
    category = await category_service.create_category(category)
    return {
        'category': category,
    }

@router.put('/categories/{category_id}', response_model=CategoryResponse)
async def update_category(category_service: CategoryDep, category_id: int, category_update: CategoryUpdate):
    category = await category_service.update_category(category_id, category_update)
    return {
        'category': category,
    }

@router.patch('/categories/{category_id}', response_model=CategoryResponse)
async def update_category_partial(
        category_service: CategoryDep, category_id: int, category_update_partial: CategoryUpdatePartial
):
    category = await category_service.update_category(category_id, category_update_partial)
    return {
        'category': category,
    }

@router.delete(
    '/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(category_service: CategoryDep, category_id: int) -> None:
    # delete_category возвращает удаляемый category, но мы используем "чистый" REST подход
    # и вернем 204 без тела ответа
    await category_service.delete_category(category_id)