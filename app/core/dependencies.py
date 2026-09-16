from fastapi import Depends
from typing import Annotated, AsyncGenerator
from app.utils.unit_of_work import UnitOfWork

async def get_uow() -> AsyncGenerator[UnitOfWork]:
    async with UnitOfWork() as uow:
        yield uow


UowDep = Annotated[UnitOfWork, Depends(get_uow)]
