from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class CategoryBase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(max_length=100)
    description: str | None = Field(max_length=1000)

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

class CategoryUpdate(CategoryBase):
    pass

class CategoryUpdatePartial(CategoryBase):
    name: str | None = None
    description: str | None = None