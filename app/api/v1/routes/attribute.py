from fastapi import APIRouter, status

from app.core.dependencies import AttributeDep
from app.api.v1.responses.attribute import AttributeResponse, AttributesResponse
from app.schemas.attribute import (
    AttributeCreate, AttributeUpdate, AttributeUpdatePartial, AttributeRead, AttributeReadWithProducts
)

router = APIRouter()

@router.get('/attributes/', summary='Get all attributes')
async def get_attributes(attribute_service: AttributeDep, with_products_articles: bool = False):
    attributes = await attribute_service.get_attributes(with_products_articles)

    schema = AttributeRead
    if with_products_articles:
        schema = AttributeReadWithProducts

    return AttributesResponse[schema](
        attributes=attributes,
        total=len(attributes)
    )

@router.get('/attributes/{attribute_id}', summary='Get attribute by id')
async def get_attribute(attribute_service: AttributeDep, attribute_id: int, with_products_articles: bool = False):
    attribute = await attribute_service.get_attribute(attribute_id, with_products_articles)

    if with_products_articles:
        return AttributeResponse[AttributeReadWithProducts](
            attribute=attribute
        )

    return AttributeResponse[AttributeRead](
        attribute=attribute
    )

@router.post(
    '/attributes/', response_model=AttributeResponse[AttributeRead], status_code=status.HTTP_201_CREATED,
    summary='Create attribute'
)
async def create_attribute(attribute_service: AttributeDep, attribute: AttributeCreate):
    attribute = await attribute_service.create_attribute(attribute)
    return {
        'attribute': attribute,
    }

@router.put(
    '/attributes/{attribute_id}', response_model=AttributeResponse[AttributeRead],
    summary='Update attribute by id'
)
async def update_attribute(attribute_service: AttributeDep, attribute_id: int, attribute_update: AttributeUpdate):
    attribute = await attribute_service.update_attribute(attribute_id, attribute_update)
    return {
        'attribute': attribute,
    }

@router.patch(
    '/attributes/{attribute_id}', response_model=AttributeResponse[AttributeRead],
    summary='Partial update attribute by id'
)
async def update_attribute_partial(
        attribute_service: AttributeDep, attribute_id: int, attribute_update_partial: AttributeUpdatePartial
):
    attribute = await attribute_service.update_attribute(attribute_id, attribute_update_partial)
    return {
        'attribute': attribute,
    }

@router.delete(
    '/attributes/{attribute_id}', status_code=status.HTTP_204_NO_CONTENT, summary='Delete attribute by id'
)
async def delete_attribute(attribute_service: AttributeDep, attribute_id: int) -> None:
    await attribute_service.delete_attribute(attribute_id)