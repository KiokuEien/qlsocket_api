from pydantic import BaseModel
from typing import Generic, TypeVar

from app.schemas.brand import BrandRead, BrandReadWithProducts

class BrandsResponse[T](BaseModel):
    success: bool = True
    total: int
    brands: list[T]

class BrandResponse[T](BaseModel):
    success: bool = True
    brand: T