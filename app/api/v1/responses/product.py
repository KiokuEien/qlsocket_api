from pydantic import BaseModel

from app.schemas.product import ProductRead, ProductReadWithAttributes

class ProductResponse[T: (ProductRead, ProductReadWithAttributes)](BaseModel):
    success: bool = True
    product: T

class ProductsResponse[T: (ProductRead, ProductReadWithAttributes)](BaseModel):
    success: bool = True
    products: list[T]