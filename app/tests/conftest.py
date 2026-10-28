import pytest
from httpx2 import AsyncClient, ASGITransport
from typing import AsyncGenerator

from app.main import app
from app.core.dependencies import get_uow, get_uow_for_tests

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    previous_overrides = app.dependency_overrides.copy()

    app.dependency_overrides[get_uow] = get_uow_for_tests
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport,
            base_url='http://test', # Условный url, например, http://test/api/v1/brands/
        ) as client:
            yield client
    finally:
        app.dependency_overrides = previous_overrides