from pydantic import BaseModel
from typing import Generic, TypeVar, Sequence

T = TypeVar('T')

class AttributesResponse(BaseModel, Generic[T]):
    success: bool = True
    total: int
    attributes: Sequence[T]

class AttributeResponse(BaseModel, Generic[T]):
    success: bool = True
    attribute: T