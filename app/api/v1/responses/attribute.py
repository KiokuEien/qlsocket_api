from pydantic import BaseModel

from app.schemas.attribute import AttributeRead

class AttributesResponse(BaseModel):
    success: bool = True
    total: int
    attributes: list[AttributeRead]

class AttributeResponse(BaseModel):
    success: bool = True
    attribute: AttributeRead