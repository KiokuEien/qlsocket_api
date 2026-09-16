from pydantic import BaseModel

from app.schemas.category import CategoryRead

class CategoriesResponse(BaseModel):
    success: bool
    total: int
    categories: list[CategoryRead]