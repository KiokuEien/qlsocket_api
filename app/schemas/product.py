from pydantic import BaseModel, ConfigDict, Field, AliasPath
from decimal import Decimal
from datetime import datetime
from typing import Any

class ProductBase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(max_length=255)
    description: str | None = None
    price: Decimal = Field(max_digits=10, decimal_places=2)
    brand_id: int
    category_id: int

class ProductCreate(ProductBase):
    attributes: dict[int, str] | None = None

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    sku: str
    created_at: datetime
    updated_at: datetime

class ProductAttributeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(validation_alias=AliasPath('attribute', 'id'))
    name: str = Field(validation_alias=AliasPath('attribute', 'name'))
    value: str

class ProductReadWithAttributes(ProductRead):
    attributes: list[ProductAttributeRead]

class ProductUpdate(ProductBase):
    attributes: dict[int, str] | None = None

class ProductUpdatePartial(ProductBase):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    price: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    brand_id: int | None = None
    category_id: int | None = None
    attributes: dict[int, str] | None = None