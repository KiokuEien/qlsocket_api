import pytest
from httpx2 import AsyncClient, ASGITransport
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.database import test_db_helper
from app.main import app
from app.core.dependencies import get_uow
from app.utils.unit_of_work import UnitOfWork

'''
pytest для каждой фикстуры client вызывает фикстуру db_session, после чего
открывается соединение к тестовой бд, создается новая сессия, она передается uow, 
после работы uow закрывает сессию, а внешняя транзакция откатывается (tx.rollback()).
'''

@pytest.fixture
async def db_session():
    async with test_db_helper.engine.connect() as conn:
        tx = await conn.begin()

        session_factory = async_sessionmaker(
            bind=conn,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            join_transaction_mode='create_savepoint',
        )

        try:
            async with session_factory() as session:
                yield session
        finally:
            await tx.rollback()


@pytest.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient]:
    async def get_uow_for_tests():
        async with UnitOfWork(session=db_session) as uow:
            yield uow

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

