from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: str | None

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