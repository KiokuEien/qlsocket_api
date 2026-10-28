from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class AttributeBase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=1000)

class AttributeCreate(AttributeBase):
    pass

class AttributeRead(AttributeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

class AttributeReadWithProducts(AttributeRead):
    products_sku: list[str]

class AttributeUpdate(AttributeBase):
    pass

class AttributeUpdatePartial(AttributeBase):
    name: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=1000)