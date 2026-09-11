from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import db_helper

'''
Unit of Work (UoW) - это объект, который управляет транзакциями и гарантирует,
что все изменения в базе данных выполняются как одно целое. Он открывает session, начинает транзакцию,
даёт возможность работать с service и repository, а в конце делает commit(), если все правильно,
или rollback(), если есть ошибка.
'''

class UnitOfWork:
    async def __aenter__(self):
        self.session: AsyncSession = db_helper.session_factory()
        # session.rollback() делает полный откат всех текущей сессии (всех транзакций)
        # tx.rollback() делает откат конкретной транзакции (система вложенных транзакций - savepoints)
        #
        self._tx = await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            await self._tx.rollback()
        else:
            await self._tx.commit()
        await self.session.close()

    # Для partial rollback
    @asynccontextmanager
    async def nested(self):
        async with self.session.begin_nested():
            yield