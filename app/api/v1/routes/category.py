from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.dependencies import UowDep
from app.schemas.category import CategoryRead
from app.services.category import CategoryService
from app.api.v1.responses.category import CategoriesResponse

router = APIRouter()

@router.get('/categories/', response_model=CategoriesResponse)
async def get_categories(uow: UowDep):
    category_service = CategoryService(uow)
    categories = await category_service.get_categories()
    return {
        'success': True,
        'total': len(categories),
        'categories': categories,
    }
