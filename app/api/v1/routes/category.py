from fastapi import APIRouter

from app.core.dependencies import CategoryDep
from app.api.v1.responses.category import CategoriesResponse, CategoryResponse

router = APIRouter()

@router.get('/categories/', response_model=CategoriesResponse)
async def get_categories(category_service: CategoryDep):
    categories = await category_service.get_categories()
    return {
        'success': True,
        'total': len(categories),
        'categories': categories,
    }

@router.get('/categories/{category_id}', response_model=CategoryResponse)
async def get_category(category_service: CategoryDep, category_id: int):
    category = await category_service.get_category(category_id=category_id)
    return {
        'success': True,
        'category': category,
    }
