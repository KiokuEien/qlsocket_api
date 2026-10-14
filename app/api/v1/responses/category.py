from typing import Any
from pydantic import BaseModel, computed_field, model_validator, model_serializer

from app.schemas.category import CategoryRead, CategoryReadWithProducts

class CategoriesResponse[T: (CategoryRead, CategoryReadWithProducts)](BaseModel):
    success: bool = True
    categories: list[T]

    # Метод 1. Самостоятельно сериализуем модель
    @model_serializer
    def serialize_model(self) -> dict[str, Any]:
        return {
            'success': self.success,
            'total': len(self.categories),
            'categories': self.categories,
        }

    # Метод 2. Динамически добавляем новое поле
    # @model_validator(mode='after')
    # def set_total(self) -> CategoriesResponse:
    #     self.total = len(self.categories)
    #     return self

    # Метод 3. Динамически добавляем вычисляемое поле (не гарантирует порядок)
    # @computed_field
    # @property
    # def total(self) -> int:
    #     return len(self.categories)


class CategoryResponse[T: (CategoryRead, CategoryReadWithProducts)](BaseModel):
    success: bool = True
    category: T