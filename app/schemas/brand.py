from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class BrandBase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(max_length=100)
    description: str | None = Field(max_length=1000)

class BrandCreate(BrandBase):
    pass

class BrandRead(BrandBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

class BrandUpdate(BrandBase):
    pass

class BrandUpdatePartial(BrandBase):
    name: str | None = None
    description: str | None = None