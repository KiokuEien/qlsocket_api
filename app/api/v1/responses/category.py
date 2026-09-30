from pydantic import BaseModel

from app.schemas.category import CategoryRead

class CategoriesResponse(BaseModel):
    success: bool = True
    total: int
    categories: list[CategoryRead]

class CategoryResponse(BaseModel):
    success: bool = True
    category: CategoryRead