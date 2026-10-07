from pydantic import BaseModel

from app.schemas.brand import BrandRead

class BrandsResponse(BaseModel):
    success: bool = True
    total: int
    brands: list[BrandRead]

class BrandResponse(BaseModel):
    success: bool = True
    brand: BrandRead