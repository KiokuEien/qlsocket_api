from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.pool import NullPool

from app.core.config import settings

class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False, use_null_pool: bool = False):
        engine_options = {
            'url': url,
            'echo': echo,
            'pool_pre_ping': True,
            'pool_recycle': 1800,
            'connect_args': {
                'timeout': 10,
                'command_timeout': 30,
                'server_settings': {
                    'application_name': 'qlsocket_api'
                }
            }
        }
        if use_null_pool:
            engine_options['poolclass'] = NullPool
        else:
            engine_options['pool_size'] = 5
            engine_options['max_overflow'] = 10

        self.engine = create_async_engine(**engine_options)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo
)

test_db_helper = DatabaseHelper(
    url=settings.test_db.url,
    echo=settings.test_db.echo,
    use_null_pool=True,
)
