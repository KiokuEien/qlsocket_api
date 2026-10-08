from fastapi import APIRouter, status

from app.core.dependencies import AttributeDep
from app.schemas.attribute import AttributeCreate, AttributeUpdate, AttributeUpdatePartial
from app.api.v1.responses.attribute import AttributesResponse, AttributeResponse

router = APIRouter()

@router.get('/attributes/', response_model=AttributesResponse, summary='Get all attributes')
async def get_attributes(attribute_service: AttributeDep):
    attributes = await attribute_service.get_attributes()
    return {
        'total': len(attributes),
        'attributes': attributes,
    }

@router.get('/attributes/{attribute_id}', response_model=AttributeResponse)
async def get_attribute(attribute_service: AttributeDep, attribute_id: int):
    attribute = await attribute_service.get_attribute(attribute_id)
    return {
        'attribute': attribute,
    }

@router.post('/attributes/', response_model=AttributeResponse, status_code=status.HTTP_201_CREATED)
async def create_attribute(attribute_service: AttributeDep, attribute: AttributeCreate):
    attribute = await attribute_service.create_attribute(attribute)
    return {
        'attribute': attribute,
    }

@router.put('/attributes/{attribute_id}', response_model=AttributeResponse)
async def update_attribute(attribute_service: AttributeDep, attribute_id: int, attribute_update: AttributeUpdate):
    attribute = await attribute_service.update_attribute(attribute_id, attribute_update)
    return {
        'attribute': attribute,
    }

@router.patch('/attributes/{attribute_id}', response_model=AttributeResponse)
async def update_attribute_partial(
        attribute_service: AttributeDep, attribute_id: int, attribute_update_partial: AttributeUpdatePartial
):
    attribute = await attribute_service.update_attribute(attribute_id, attribute_update_partial)
    return {
        'attribute': attribute,
    }

@router.delete(
    '/attributes/{attribute_id}', status_code=status.HTTP_204_NO_CONTENT
)
async def delete_attribute(attribute_service: AttributeDep, attribute_id: int) -> None:
    await attribute_service.delete_attribute(attribute_id)